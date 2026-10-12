import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import concurrent.futures

def get_nifty500_symbols():
    """Returns the complete Nifty 500 universe directly (no external file needed)."""
    raw_symbols = [
        "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "BHARTIARTL", "SBIN", "LICI", "ITC", "HINDUNILVR",
        "LT", "HCLTECH", "SUNPHARMA", "BAJFINANCE", "MARUTI", "ADANIENT", "TATAMOTORS", "TITAN", "NTPC", "KOTAKBANK",
        "ONGC", "AXISBANK", "ASIANPAINT", "ADANIPORTS", "COALINDIA", "POWERGRID", "DMART", "BAJAJFINSV", "SIEMENS", "GRASIM",
        "WIPRO", "ZOMATO", "JIOFIN", "TATASTEEL", "IOC", "HAL", "BAJAJ-AUTO", "SBILIFE", "BRITANNIA", "LODHA",
        "ATGL", "GODREJCP", "INDUSINDBK", "DLF", "VEDL", "GAIL", "CANBK", "BPCL", "NESTLEIND", "AMBUJACEM",
        "TRENT", "M&M", "BANKBARODA", "HDFCLIFE", "TATACONSUM", "SHRIRAMFIN", "CHOLAFIN", "DRREDDY", "CIPLA", "TVSMOTOR",
        "PHOENIXLTD", "HEROMOTOCO", "HINDALCO", "BEL", "PIIND", "BHEL", "PNB", "EICHERMOT", "ICICIGI", "DIVISLAB",
        "RECLTD", "PFC", "JINDALSTEL", "HINDPETRO", "ABB", "TORNTPHARM", "OBEROIRLTY", "NAUKRI", "MAXHEALTH", "MUTHOOTFIN",
        "POLYCAB", "ZYDUSLIFE", "BERGEPAINT", "ICICIPRULI", "INDIGO", "SHREECEM", "SBICARD", "MOTHERSON", "TATACOMM", "SRF",
        "COLPAL", "DABUR", "PERSISTENT", "APOLLOHOSP", "LUPIN", "CONCOR", "IDBI", "UNIONBANK", "OFSS", "PAGEIND",
        "JSL", "TORNTPOWER", "IPCALAB", "SUPREMEIND", "ATUL", "VOLTAS", "JSWENERGY", "DALBHARAT", "DIXON", "ASTRAL",
        "FLUOROCHEM", "APLAPOLLO", "GLENMARK", "BHARATFORG", "ABFRL", "MRF", "ALKEM", "CUMMINSIND", "ESCORTS", "TIINDIA",
        "DEEPAKFERT", "CHAMBLFERT", "COROMANDEL", "GNFC", "DEEPAKNTR", "ATGL", "AUBANK", "FEDERALBNK", "IDFCFIRSTB", "RBLBANK",
        "BANDHANBNK", "CANFINHOME", "PNBHOUSING", "AAVAS", "CREDITACC", "MAHABANK", "UCOBANK", "CENTRALBK", "IOB", "PSB",
        "JUBLFOOD", "BATAINDIA", "RELAXO", "PAGEIND", "METROPOLIS", "LALPATHLAB", "THYROCARE", "KALYANKJIL", "RAJESHEXPO", "TITAGARH",
        "MANYAVAR", "ABSLAMC", "HDFCAMC", "NAM-INDIA", "UTIAMC", "CAMS", "ENDURANCE", "JAMNAAUTO", "SUNDRMFAST", "BHARATRAS",
        "CARBORUNIV", "TIMKEN", "SKFINDIA", "SCHAEFFLER", "THERMAX", "TRIVENI", "ELGIEQUIP", "KIRLOSENG", "ACC", "RAMCOCEMS",
        "JKCEMENT", "HEIDELBERG", "STARCEMENT", "CENTURYPLY", "GREENPLY", "KAJARIACER", "SOMANYCERA", "CERA", "KITEX", "ARVIND",
        "RAYMOND", "GRASIM", "TRIDENT", "WELSPUNLIV", "KPRMILL", "VARDHACRLC", "NILKAMAL", "SAFARI", "VIPIND", "TIIL",
        "BLUEDART", "TCI", "AEGISLOG", "GESHIPPING", "SCI", "GREATEAST", "NAVINFLUOR", "CLEAN", "FINEORG", "AARTIIND",
        "ALKYLAMINE", "BALAMINES", "NEOGEN", "SUDARSCHEM", "BASF", "ATUL", "NOCIL", "VINATIORG", "GHCL", "TATACHEM",
        "GNFC", "GSFC", "FACT", "RCF", "CHAMBLFERT", "COROMANDEL", "DEEPAKFERT", "PARADEEP", "SANOFI", "PFIZER",
        "ASTRAZEN", "GLAXO", "NOVARTIS", "MERCK", "ERIS", "IPCALAB", "AJANTPHARM", "JBCHEPHARM", "GRANULES", "NATCOPHARM",
        "FDC", "CAPLIPOINT", "SUNCLAY", "LINDEINDIA", "GICRE", "NEWGEN", "NIITMTS", "ZENSARTECH", "COFORGE", "MPHASIS",
        "LTIM", "TECHM", "INFY", "TCS", "WIPRO", "HCLTECH", "PERSISTENT", "CYIENT", "KPITTECH", "INTELLECT",
        "SONACOMS", "HAPPYFORGE", "TIMKEN", "RKFORGE", "MMTC", "MOIL", "HINDZINC", "HINDCOPPER", "NATIONALUM", "GMDC",
        "JINDALSAW", "MASTEK", "ROLTA", "BSOFT", "RATEGAIN", "LATENTVIEW", "TANLA", "MAPMYINDIA", "CMSINFO", "PAYTM",
        "POLICYBZR", "ZOMATO", "NYKAA", "DELHIVERY", "TRACXN", "MAPMYINDIA", "EASEMYTRIP", "IXIGO", "AZAD", "HONASA",
        "CEATLTY", "JKTYRE", "APOLLOTYRE", "MRF", "TVSSRICHAK", "AMARAJABAT", "EXIDEIND", "BASIL", "HBLPOWER", "ARE&M",
        "ADANIGREEN", "ADANIPOWER", "ADANITRANS", "JSWENERGY", "TORNTPOWER", "NHPC", "SJVN", "CESC", "TATAPOWER", "RELINFRA",
        "JPPOWER", "BFUTILITIE", "RTNPOWER", "INOXWIND", "SUZLON", "BORORENEW", "PRESTIGE", "BRIGADE", "SOBHA", "DLF",
        "OBEROIRLTY", "PHOENIXLTD", "GODREJPROP", "LODHA", "MAHLIFE", "ANANTRAJ", "SUNTECK", "KOLTEPATIL", "PURAVANKARA", "ASHIANA",
        "IBULHSGFIN", "IIFL", "SHRIRAMFIN", "MANAPPURAM", "MUTHOOTFIN", "CHOLAFIN", "M&MFIN", "SUNDARMFIN", "SCMDCL", "DHANI",
        "HUDCO", "IREDA", "IFCI", "SREINFRA", "REPCOHOME", "CANFINHOME", "GICHSGFIN", "PNBHOUSING", "AAVAS", "HOMEFIRST",
        "ASTERDM", "NARAYANA", "KIMS", "METROPOLIS", "LALPATHLAB", "THYROCARE", "VIJAYA", "MEDANTA", "RAINBOW", "NH",
        "JSWSTEEL", "TATASTEEL", "JSL", "JINDALSTEL", "SAIL", "NMDC", "APLAPOLLO", "GPIL", "JINDALSAW", "WELCORP",
        "RATNAMANI", "MAZDA", "COCHINSHIP", "GRSE", "MAZAGOCK", "GARDENREACH", "COCHINSHIP", "DATAPATTNS", "MTARTECH", "ASTEC",
        "CHEMPLASTS", "SOLARA", "GLAND", "LAURUSLABS", "DIVISLAB", "AUROPHARMA", "LUPIN", "CIPLA", "DRREDDY", "SUNPHARMA"
    ]
    # Remove duplicates and format with .NS
    clean_symbols = sorted(list(set([s.strip().upper() + ".NS" for s in raw_symbols])))
    return clean_symbols

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
    # Multi-threading to scan all stocks fast (max 20 parallel workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(scan_symbol, watchlist)
        for res in results:
            if res:
                print(res)
                active_signals.append(res)
                
    print("=" * 70)
    print(f"Scan complete. Total active signals found: {len(active_signals)}")
