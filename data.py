import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
import config
import logging
import time

_client = None

def get_binance_client():
    """Khởi tạo và trả về Binance client."""
    global _client
    if _client is None:
        _client = Client(api_key=config.BINANCE_API_KEY, api_secret=config.BINANCE_API_SECRET)
    return _client

def get_all_symbols():
    """Lấy tất cả các cặp giao dịch USDT trên Binance Futures."""
    client = get_binance_client()
    try:
        exchange_info = client.futures_exchange_info()
        symbols = [
            s['symbol'] for s in exchange_info['symbols']
            if s['symbol'].endswith('USDT') and s['status'] == 'TRADING'
        ]
        return symbols
    except BinanceAPIException as e:
        logging.error(f"❌ Lỗi Binance API khi lấy danh sách symbol: {e}")
        from alert import alert_telegram_on_error
        alert_telegram_on_error(f"Lỗi Binance API khi lấy danh sách symbol: {e}")
        return []
    except Exception as e:
        logging.error(f"❌ Lỗi không xác định khi lấy danh sách symbol: {e}")
        from alert import alert_telegram_on_error
        alert_telegram_on_error(f"Lỗi không xác định khi lấy danh sách symbol: {e}")
        return []

def get_klines(symbol: str, interval: str, limit: int = 200):
    """
    Lấy dữ liệu nến (klines) từ Binance Futures.

    Args:
        symbol (str): Cặp giao dịch (ví dụ: BTCUSDT).
        interval (str): Khung thời gian nến (ví dụ: 1h, 4h).
        limit (int): Số lượng nến muốn lấy.

    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu nến.
    """
    client = get_binance_client()
    try:
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        df = df.set_index('open_time')
        
        # Chuyển đổi các cột số sang định dạng số
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        return df
    except BinanceAPIException as e:
        # Xử lý lỗi cụ thể của Binance API
        logging.error(f"❌ Lỗi Binance API khi lấy klines cho {symbol}, interval {interval}: {e}")
        from alert import alert_telegram_on_error
        alert_telegram_on_error(f"Lỗi Binance API khi lấy klines cho {symbol}, interval {interval}: {e}")
        if "Too much request" in str(e): # Xử lý Rate Limit
            logging.warning("⚠️ Đã đạt giới hạn request, tạm dừng 60 giây...")
            time.sleep(60)
        return pd.DataFrame() # Trả về DataFrame rỗng khi có lỗi
    except Exception as e:
        logging.error(f"❌ Lỗi không xác định khi lấy klines cho {symbol}: {e}")
        from alert import alert_telegram_on_error
        alert_telegram_on_error(f"Lỗi không xác định khi lấy klines cho {symbol}: {e}")
        return pd.DataFrame() # Trả về DataFrame rỗng khi có lỗi