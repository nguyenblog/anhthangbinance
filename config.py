import os
from dotenv import load_dotenv

load_dotenv() # Load biến môi trường từ .env

# 🧪 Chế độ DEV
IS_DEV = os.getenv("IS_DEV", "False").lower() == "true"

# 🔐 Binance API
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Luôn kiểm tra BINANCE_API_KEY và BINANCE_API_SECRET
if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    raise ValueError("❌ Vui lòng cấu hình BINANCE_API_KEY và BINANCE_API_SECRET trong .env")

# 📢 Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Luôn kiểm tra TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("❌ Vui lòng cấu hình TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID trong .env")

# ⏰ Cấu hình thời gian chạy bot
TIME_INTERVAL = int(os.getenv("TIME_INTERVAL", "1")) # Mặc định là 1 giờ/phút
TIME_INTERVAL_UNIT = os.getenv("TIME_INTERVAL_UNIT", "hours").lower() # "minutes" hoặc "hours"

CANDLE_LIMIT = int(os.getenv("CANDLE_LIMIT", "200")) # Số lượng nến để phân tích

# Cấu hình riêng cho từng khung thời gian
CANDLE_INTERVAL_1H = "1h" # Khung thời gian nến cho bot 1H
CANDLE_INTERVAL_4H = "4h" # Khung thời gian nến cho bot 4H
CANDLE_INTERVAL_1D = "1d" # Khung thời gian nến cho bot 1D

# 🧪 Cấu hình TEST MODE
TEST_COINS = os.getenv("TEST_COINS", "BTCUSDT,ETHUSDT") # Danh sách coin test, cách nhau bởi dấu phẩy

# ⚙️ Cấu hình chiến lược (1H)
RSI_LOWER_1H = int(os.getenv("RSI_LOWER_1H", "40"))
RSI_UPPER_1H = int(os.getenv("RSI_UPPER_1H", "60"))
PRICE_BUFFER_1H = float(os.getenv("PRICE_BUFFER_1H", "1.002")) 
VOLUME_LOOKBACK_1H = int(os.getenv("VOLUME_LOOKBACK_1H", "3")) # Số nến volume xanh liên tiếp cần kiểm tra

# ⚙️ Cấu hình chiến lược (4H)
RSI_LOWER_4H = int(os.getenv("RSI_LOWER_4H", "40"))
RSI_UPPER_4H = int(os.getenv("RSI_UPPER_4H", "60"))
PRICE_BUFFER_4H = float(os.getenv("PRICE_BUFFER_4H", "1.002")) 
VOLUME_LOOKBACK_4H = int(os.getenv("VOLUME_LOOKBACK_4H", "3")) # Số nến volume xanh liên tiếp cần kiểm tra

# ⚙️ Cấu hình chiến lược (1D) - MỚI BỔ SUNG
RSI_LOWER_1D = int(os.getenv("RSI_LOWER_1D", "40"))
RSI_UPPER_1D = int(os.getenv("RSI_UPPER_1D", "60"))
PRICE_BUFFER_1D = float(os.getenv("PRICE_BUFFER_1D", "1.002")) 
VOLUME_LOOKBACK_1D = int(os.getenv("VOLUME_LOOKBACK_1D", "3")) # Số nến volume xanh liên tiếp cần kiểm tra