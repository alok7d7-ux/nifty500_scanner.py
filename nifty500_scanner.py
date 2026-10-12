import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import concurrent.futures
import requests
import io

def get_nifty500_symbols():
    """Fetches the full Nifty 500 list from a reliable public mirror raw CSV."""
    url = "https://raw.githubusercontent.com/kprohith/nse-stock-analysis/master/ind_nifty500list.csv"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            if 'Symbol' in df.columns:
                symbols = df['Symbol'].dropna().unique().tolist()
                return [s.strip().upper() + ".NS" for s in symbols]
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        
    # Ultimate fallback if network fails completely
    fallback = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", "ITC", "KOTAKBANK", "LT"]
    return [s + ".NS" for s in fallback]

def calculate_atr(df, period=5):
    """Calculates Average True Range (ATR) with period 5."""
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def generate_renko_bricks(df, atr_period=5, atr_mult=3.0):
    """Converts OHLC dataframe into ATR-based Renko bricks (ATR 5, Mult 3)."""
    atr = calculate_atr(df, atr_period)
    if atr.dropna().empty:
        return None, 0
    brick_size = atr.dropna().iloc[-1] * atr_mult
    
    if pd.isna(brick_size) or brick_size == 0:
        return None, 0
    
    renko_bars = []
    prev_close = df['Close'].iloc[0]
    
    for current_price in df['Close']:
        diff = current_price - prev_close
        if abs(diff) >= brick_size:
            num_bricks = int(abs(diff) // brick_size)
            direction = 1 if diff > 0 else -1
            
            for _ in range(num_bricks):
                open_p = prev_close
                close_p = open_p + (direction * brick_size)
                high_p = max(open_p, close_p)
                low_p = min(open_p, close_p)
                
                renko_bars.append({
                    'Open': open_p, 'High': high_p, 'Low': low_p, 'Close': close_p, 'Direction': direction
                })
                prev_close = close_p
                
    return pd.DataFrame(renko_bars), brick_size

def calculate_supertrend(df, period, multiplier):
    """Calculates Supertrend bands and trend direction."""
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - df['Close'].shift()).abs()
    tr3 = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/period, min_periods=period).mean()

    hl2 = (df['High'] + df['Low']) / 2
    basic_ub = hl2 + (multiplier * atr)
    basic_lb = hl2 - (multiplier * atr)

    final_ub = pd.Series(0.0, index=df.index)
    final_lb = pd.Series(0.0, index=df.index)
    supertrend = pd.Series(True, index=df.index)

    for i in range(1, len(df)):
        if basic_ub.iloc[i] < final_ub.iloc[i-1] or df['Close'].iloc[i-1] > final_ub.iloc[i-1]:
            final_ub.iloc[i] = basic_ub.iloc[i]
        else:
            final_ub.iloc[i] = final_ub.iloc[i-1]

        if basic_lb.iloc[i] > final_lb.iloc[i-1] or df['Close'].iloc[i-1] < final_lb.iloc[i-1]:
            final_lb.iloc[i] = basic_lb.iloc[i]
        else:
            final_lb.iloc[i] = final_lb.iloc[i-1]

        if supertrend.iloc[i-1] and df['Close'].iloc[i] < final_lb.iloc[i]:
            supertrend.iloc[i] = False
        elif not supertrend.iloc[i-1] and df['Close'].iloc[i] > final_ub.iloc[i]:
            supertrend.iloc[i] = True
        else:
            supertrend.iloc[i] = supertrend.iloc[i-1]

    return supertrend

def scan_symbol(symbol):
    """Scans individual symbol for 10-minute Renko + Triple Supertrend 1-3 brick signals."""
    try:
        data = yf.download(symbol, period="5d", interval="5m", progress=False)
        if data.empty:
            return None
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Resample 5m to 10m bars
        df_10m = data.resample('10min').agg({
            'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'
        }).dropna()

        renko_df, brick_size = generate_renko_bricks(df_10m, atr_period=5, atr_mult=3.0)
        if renko_df is None or len(renko_df) < 25:
            return None

        # Triple Supertrend Inputs: 10.2, 10.3, 21.1
        st1 = calculate_supertrend(renko_df, period=10, multiplier=2.0)
        st2 = calculate_supertrend(renko_df, period=10, multiplier=3.0)
        st3 = calculate_supertrend(renko_df, period=21, multiplier=1.0)

        renko_df['All_Bullish'] = st1 & st2 & st3
        renko_df['All_Bearish'] = (~st1) & (~st2) & (~st3)

        # Check signal age: 1 to 3 bricks old
        for brick_age in range(1, 4):
            idx = -brick_age
            if idx - 1 < -len(renko_df):
                break
                
            if renko_df['All_Bullish'].iloc[idx] and not renko_df['All_Bullish'].iloc[idx - 1]:
                return f"🚀 [BUY] {symbol} | Price: {renko_df['Close'].iloc[-1]:.2f} | Triggered {brick_age} brick(s) ago"

            if renko_df['All_Bearish'].iloc[idx] and not renko_df['All_Bearish'].iloc[idx - 1]:
                return f"📉 [SELL] {symbol} | Price: {renko_df['Close'].iloc[-1]:.2f} | Triggered {brick_age} brick(s) ago"
                
    except Exception:
        pass
    return None

if __name__ == "__main__":
    print("=" * 70)
    print(f" NIFTY 500 RENKO + TRIPLE SUPERTREND SCANNER | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    watchlist = get_nifty500_symbols()
    print(f"Loaded {len(watchlist)} symbols from Nifty 500 universe. Scanning concurrently...")
    
    active_signals = []
    # Multi-threading to scan 500 stocks fast (max 20 parallel workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(scan_symbol, watchlist)
        for res in results:
            if res:
                print(res)
                active_signals.append(res)
                
    print("=" * 70)
    print(f"Scan complete. Total active signals found: {len(active_signals)}")
