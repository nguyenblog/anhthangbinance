import pandas as pd
import numpy as np 

def add_all_indicators(df: pd.DataFrame, short: int, long: int):
    """
    Thêm tất cả các chỉ báo kỹ thuật cần thiết vào DataFrame.
    - MA ngắn hạn (MA_Short)
    - MA dài hạn (MA_Long)
    - RSI
    - MACD (MACD_Line, Signal_Line, Histogram)
    """
    # 1. Moving Averages (MA) - Đường trung bình động
    df["MA_Short"] = df["close"].rolling(window=short).mean()
    df["MA_Long"] = df["close"].rolling(window=long).mean()

    # 2. Relative Strength Index (RSI)
    delta = df["close"].diff(1)
    
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=13, adjust=False).mean() 
    avg_loss = loss.ewm(com=13, adjust=False).mean() 

    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], np.nan) 

    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi

    # 3. Moving Average Convergence Divergence (MACD)
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()

    macd_line = exp1 - exp2

    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    histogram = macd_line - signal_line

    df["MACD_Line"] = macd_line
    df["Signal_Line"] = signal_line
    df["MACD_Histogram"] = histogram

    return df