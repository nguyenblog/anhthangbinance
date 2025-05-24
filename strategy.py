import pandas as pd
import config
import numpy as np 

# Hàm trợ giúp để xác định volume là "xanh" hay "đỏ"
def is_green_volume(df: pd.DataFrame, current_idx: int) -> bool:
    """
    Kiểm tra xem volume của nến tại current_idx có phải là "volume xanh" hay không.
    Volume xanh = giá đóng cửa của nến hiện tại cao hơn giá đóng cửa của nến trước đó.
    """
    # Đảm bảo có nến trước đó để so sánh (current_idx phải lớn hơn 0 nếu dùng index dương,
    # hoặc abs(current_idx) < len(df) - 1 nếu dùng index âm)
    if abs(current_idx) >= len(df) - 1: # current_idx = -2 nghĩa là phần tử thứ len(df)-2. cần nến len(df)-3
        return False
    
    # current_close là giá đóng cửa của nến đang xét
    current_close = df["close"].iloc[current_idx]
    # prev_close là giá đóng cửa của nến ngay trước đó
    prev_close = df["close"].iloc[current_idx - 1] # Index âm: -2 - 1 = -3 (nến trước đó)
    
    return current_close > prev_close

# Hàm kiểm tra điều kiện cho khung 4H
def check_conditions_4h(df: pd.DataFrame):
    idx = -2 # Lấy nến đã đóng cửa gần nhất (nến hiện tại là -1)

    # Đảm bảo đủ dữ liệu nến cho tất cả chỉ báo VÀ VOLUME_LOOKBACK để kiểm tra volume xanh
    # Cần số lượng nến tối đa cho chỉ báo + số nến cần kiểm tra volume xanh + 1 nến nữa để so sánh
    required_klines_for_indicators = max(20, 50, 26) + config.VOLUME_LOOKBACK_4H + 1 
    
    if len(df) < required_klines_for_indicators:
        return {"error": f"Không đủ dữ liệu nến ({len(df)} < {required_klines_for_indicators}) cho khung 4H để tính toán chỉ báo và volume."}, False, {}

    # Kiểm tra NaN sau khi add_all_indicators đã chạy
    if pd.isna(df["MA_Short"].iloc[idx]) or \
       pd.isna(df["MA_Long"].iloc[idx]) or \
       pd.isna(df["RSI"].iloc[idx]) or \
       pd.isna(df["MACD_Line"].iloc[idx]) or \
       pd.isna(df["Signal_Line"].iloc[idx]):
        return {"error": "Chỉ báo không hợp lệ (NaN) cho khung 4H"}, False, {}


    current_price = df["close"].iloc[idx]
    ma_short_value = df["MA_Short"].iloc[idx] # Tương ứng với MA20
    ma_long_value = df["MA_Long"].iloc[idx]   # Tương ứng với MA50
    rsi = df["RSI"].iloc[idx]
    macd_line = df["MACD_Line"].iloc[idx]
    signal_line = df["Signal_Line"].iloc[idx]

    # --- LOGIC VOLUME MỚI: KIỂM TRA VOLUME XANH ---
    volume_green_condition = True
    
    # extra_info sẽ chứa thông tin chi tiết về từng nến volume
    volume_color_info_list = []

    # Duyệt từ nến đã đóng cửa gần nhất (idx = -2) về trước
    # range(config.VOLUME_LOOKBACK_4H) sẽ lặp 0, 1, ..., VOLUME_LOOKBACK_4H-1
    # Để kiểm tra N nến, chúng ta cần duyệt từ idx về idx - (N-1)
    
    for i in range(config.VOLUME_LOOKBACK_4H):
        candle_index_to_check = idx - i
        
        # Đảm bảo index hợp lệ cho cả nến hiện tại và nến trước đó để so sánh
        if abs(candle_index_to_check) >= len(df) or abs(candle_index_to_check - 1) >= len(df):
            volume_green_condition = False # Không đủ dữ liệu để kiểm tra nến này
            break

        is_gv = is_green_volume(df, candle_index_to_check)
        
        volume_color_info_list.append({
            "idx": candle_index_to_check,
            "volume": df["volume"].iloc[candle_index_to_check],
            "close_current": df["close"].iloc[candle_index_to_check],
            "close_prev": df["close"].iloc[candle_index_to_check - 1],
            "is_green_volume": is_gv
        })

        if not is_gv: # Nếu một nến không phải volume xanh
            volume_green_condition = False
            break # Dừng kiểm tra vì điều kiện đã sai
            
    # --- KẾT THÚC LOGIC VOLUME MỚI ---

    # Kiểm tra điều kiện
    ma_condition = ma_short_value > ma_long_value
    price_condition = ma_short_value < current_price <= ma_short_value * config.PRICE_BUFFER_4H
    rsi_condition = config.RSI_LOWER_4H <= rsi <= config.RSI_UPPER_4H
    macd_condition = macd_line > signal_line
    volume_condition = volume_green_condition # <-- SỬ DỤNG ĐIỀU KIỆN VOLUME XANH

    conditions_4h = {
        "ma_condition": ma_condition,
        "price_condition": price_condition,
        "rsi_condition": rsi_condition,
        "macd_condition": macd_condition,
        "volume_condition": volume_condition, 
    }

    all_passed = all(conditions_4h.values())

    extra_info = {
        "price": current_price,
        "ma_short": ma_short_value,
        "ma_long": ma_long_value,
        "rsi": rsi,
        "dif": macd_line,
        "dea": signal_line,
        "volume_now": df["volume"].iloc[idx], # Volume của nến đang xét (nến -2)
        "volume_color_info": volume_color_info_list # Thông tin chi tiết cho debug
    }

    return conditions_4h, all_passed, extra_info

# Hàm kiểm tra điều kiện cho khung 1H
def check_conditions_1h(df: pd.DataFrame):
    idx = -2 # Lấy nến đã đóng cửa gần nhất (nến hiện tại là -1)

    # Đảm bảo đủ dữ liệu nến cho tất cả chỉ báo VÀ VOLUME_LOOKBACK để kiểm tra volume xanh
    required_klines_for_indicators = max(9, 21, 26) + config.VOLUME_LOOKBACK_1H + 1
    
    if len(df) < required_klines_for_indicators:
        return {"error": f"Không đủ dữ liệu nến ({len(df)} < {required_klines_for_indicators}) cho khung 1H để tính toán chỉ báo và volume."}, False, {}

    # Kiểm tra NaN sau khi add_all_indicators đã chạy
    if pd.isna(df["MA_Short"].iloc[idx]) or \
       pd.isna(df["MA_Long"].iloc[idx]) or \
       pd.isna(df["RSI"].iloc[idx]) or \
       pd.isna(df["MACD_Line"].iloc[idx]) or \
       pd.isna(df["Signal_Line"].iloc[idx]):
        return {"error": "Chỉ báo không hợp lệ (NaN) cho khung 1H"}, False, {}


    current_price = df["close"].iloc[idx]
    ma_short_value = df["MA_Short"].iloc[idx] # Tương ứng với MA9
    ma_long_value = df["MA_Long"].iloc[idx]   # Tương ứng với MA21
    rsi = df["RSI"].iloc[idx]
    macd_line = df["MACD_Line"].iloc[idx]
    signal_line = df["Signal_Line"].iloc[idx]

    # --- LOGIC VOLUME MỚI: KIỂM TRA VOLUME XANH ---
    volume_green_condition = True
    volume_color_info_list = []

    for i in range(config.VOLUME_LOOKBACK_1H):
        candle_index_to_check = idx - i
        
        if abs(candle_index_to_check) >= len(df) or abs(candle_index_to_check - 1) >= len(df):
            volume_green_condition = False
            break

        is_gv = is_green_volume(df, candle_index_to_check)
        
        volume_color_info_list.append({
            "idx": candle_index_to_check,
            "volume": df["volume"].iloc[candle_index_to_check],
            "close_current": df["close"].iloc[candle_index_to_check],
            "close_prev": df["close"].iloc[candle_index_to_check - 1],
            "is_green_volume": is_gv
        })

        if not is_gv:
            volume_green_condition = False
            break 
    # --- KẾT THÚC LOGIC VOLUME MỚI ---

    # Kiểm tra điều kiện
    ma_condition = ma_short_value > ma_long_value
    price_condition = ma_short_value < current_price <= ma_short_value * config.PRICE_BUFFER_1H
    rsi_condition = config.RSI_LOWER_1H <= rsi <= config.RSI_UPPER_1H
    macd_condition = macd_line > signal_line
    volume_condition = volume_green_condition 

    conditions_1h = {
        "ma_condition": ma_condition,
        "price_condition": price_condition,
        "rsi_condition": rsi_condition,
        "macd_condition": macd_condition,
        "volume_condition": volume_condition, 
    }

    all_passed = all(conditions_1h.values())

    extra_info = {
        "price": current_price,
        "ma_short": ma_short_value,
        "ma_long": ma_long_value,
        "rsi": rsi,
        "dif": macd_line,
        "dea": signal_line,
        "volume_now": df["volume"].iloc[idx],
        "volume_color_info": volume_color_info_list
    }

    return conditions_1h, all_passed, extra_info


# Hàm kiểm tra điều kiện cho khung 1D - MỚI BỔ SUNG
def check_conditions_1d(df: pd.DataFrame):
    idx = -2 # Lấy nến đã đóng cửa gần nhất (nến hiện tại là -1)

    # Đảm bảo đủ dữ liệu nến cho tất cả chỉ báo VÀ VOLUME_LOOKBACK để kiểm tra volume xanh
    required_klines_for_indicators = max(20, 50, 26) + config.VOLUME_LOOKBACK_1D + 1 # Có thể dùng MA khác cho D1 nếu muốn
    
    if len(df) < required_klines_for_indicators:
        return {"error": f"Không đủ dữ liệu nến ({len(df)} < {required_klines_for_indicators}) cho khung 1D để tính toán chỉ báo và volume."}, False, {}

    # Kiểm tra NaN sau khi add_all_indicators đã chạy
    if pd.isna(df["MA_Short"].iloc[idx]) or \
       pd.isna(df["MA_Long"].iloc[idx]) or \
       pd.isna(df["RSI"].iloc[idx]) or \
       pd.isna(df["MACD_Line"].iloc[idx]) or \
       pd.isna(df["Signal_Line"].iloc[idx]):
        return {"error": "Chỉ báo không hợp lệ (NaN) cho khung 1D"}, False, {}


    current_price = df["close"].iloc[idx]
    ma_short_value = df["MA_Short"].iloc[idx] # Tương ứng với MA20
    ma_long_value = df["MA_Long"].iloc[idx]   # Tương ứng với MA50
    rsi = df["RSI"].iloc[idx]
    macd_line = df["MACD_Line"].iloc[idx]
    signal_line = df["Signal_Line"].iloc[idx]

    # --- LOGIC VOLUME MỚI: KIỂM TRA VOLUME XANH ---
    volume_green_condition = True
    volume_color_info_list = []

    for i in range(config.VOLUME_LOOKBACK_1D):
        candle_index_to_check = idx - i
        
        if abs(candle_index_to_check) >= len(df) or abs(candle_index_to_check - 1) >= len(df):
            volume_green_condition = False
            break

        is_gv = is_green_volume(df, candle_index_to_check)
        
        volume_color_info_list.append({
            "idx": candle_index_to_check,
            "volume": df["volume"].iloc[candle_index_to_check],
            "close_current": df["close"].iloc[candle_index_to_check],
            "close_prev": df["close"].iloc[candle_index_to_check - 1],
            "is_green_volume": is_gv
        })

        if not is_gv:
            volume_green_condition = False
            break 
    # --- KẾT THÚC LOGIC VOLUME MỚI ---

    # Kiểm tra điều kiện
    ma_condition = ma_short_value > ma_long_value
    price_condition = ma_short_value < current_price <= ma_short_value * config.PRICE_BUFFER_1D
    rsi_condition = config.RSI_LOWER_1D <= rsi <= config.RSI_UPPER_1D
    macd_condition = macd_line > signal_line
    volume_condition = volume_green_condition 

    conditions_1d = {
        "ma_condition": ma_condition,
        "price_condition": price_condition,
        "rsi_condition": rsi_condition,
        "macd_condition": macd_condition,
        "volume_condition": volume_condition, 
    }

    all_passed = all(conditions_1d.values())

    extra_info = {
        "price": current_price,
        "ma_short": ma_short_value,
        "ma_long": ma_long_value,
        "rsi": rsi,
        "dif": macd_line,
        "dea": signal_line,
        "volume_now": df["volume"].iloc[idx],
        "volume_color_info": volume_color_info_list
    }

    return conditions_1d, all_passed, extra_info


# format_telegram_message - cập nhật mô tả volume
def format_telegram_message(matched_coins_info, timeframe):
    """
    Định dạng tin nhắn Telegram từ danh sách các coin thỏa mãn điều kiện.
    Thêm link tới Binance Futures.
    """
    messages = []
    if not matched_coins_info:
        return f"❗[Thời gian: {timeframe}] Không có đồng coin nào thỏa mãn điều kiện."

    for info in matched_coins_info:
        symbol = info.get("symbol", "N/A")
        binance_trade_url = f"https://www.binance.com/en/futures/{symbol}"
        msg = f"{symbol}: {binance_trade_url}"
        messages.append(msg)
    return "\n".join(messages)