import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import concurrent.futures
import requests
import io

def get_nifty500_symbols():
    """Fetches the official Nifty 500 list directly from NSE archives with robust headers."""
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            # The official NSE CSV uses 'Symbol' column
            if 'Symbol' in df.columns:
                symbols = df['Symbol'].dropna().unique().tolist()
                return [s.strip().upper() + ".NS" for s in symbols]
    except Exception as e:
        print(f"Error fetching from NSE: {e}")
        
    # Backup fallback source if NSE blocks the request
    backup_url = "https://raw.githubusercontent.com/shashankkhanagoudar/nifty-500-list/main/nifty500.csv"
    try:
        response = requests.get(backup_url, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            col = 'Symbol' if 'Symbol' in df.columns else df.columns[0]
            symbols = df[col].dropna().unique().tolist()
            return [s.strip().upper() + ".NS" for s in symbols]
    except Exception:
        pass

    # Ultimate fallback key index stocks
    print("Warning: Using fallback major stocks list.")
    fallback = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL", "ITC", "KOTAKBANK", "LT"]
    return [s + ".NS" for s in fallback]

# (Keep all your existing calculate_atr, generate_renko_bricks, calculate_supertrend, and scan_symbol functions below this...)
