# 📝 Hướng dẫn cấu hình file .env

## 1. Giới thiệu
File `.env` chứa tất cả cấu hình quan trọng để bot hoạt động. **Không chia sẻ file này** vì nó chứa thông tin nhạy cảm như API Key.

## 2. Cách tạo file .env
1. Sao chép file `.env.example` (nếu có) thành `.env`
2. Hoặc tạo file mới tên `.env` trong cùng thư mục với file `.exe` hoặc mã nguồn

## 3. Giải thích các thông số

### 🔐 Thông tin bắt buộc
```env
# Binance API Key - Lấy từ tài khoản Binance của bạn
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here

# Telegram Bot - Để nhận thông báo
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### ⚙️ Cấu hình chung
```env
# Chế độ phát triển (True: test với TEST_COINS, False: quét tất cả coin)
IS_DEV=True
TEST_COINS=BTCUSDT,ETHUSDT  # Các coin dùng để test, cách nhau bởi dấu phẩy

# Thời gian chạy bot (tính bằng phút/giờ)
TIME_INTERVAL=60
TIME_INTERVAL_UNIT=minutes  # minutes hoặc hours

# Số nến tối đa để phân tích
CANDLE_LIMIT=400
```

### 📊 Cấu hình chiến lược theo khung thời gian

#### Khung 1H
```env
RSI_LOWER_1H=40      # Ngưỡng RSI thấp
RSI_UPPER_1H=60      # Ngưỡng RSI cao
PRICE_BUFFER_1H=1.002 # Chênh lệch giá tối đa so với MA (1.002 = 0.2%)
VOLUME_LOOKBACK_1H=3  # Số nến volume xanh liên tiếp cần kiểm tra
```

#### Khung 4H
```env
RSI_LOWER_4H=40
RSI_UPPER_4H=60
PRICE_BUFFER_4H=1.002
VOLUME_LOOKBACK_4H=3
```

#### Khung 1D
```env
RSI_LOWER_1D=40
RSI_UPPER_1D=60
PRICE_BUFFER_1D=1.002
VOLUME_LOOKBACK_1D=3
```

## 4. Hướng dẫn lấy thông tin

### Lấy Binance API Key
1. Đăng nhập vào tài khoản Binance
2. Vào [API Management](https://www.binance.com/en/my/settings/api-management)
3. Tạo API Key mới (chỉ cần quyền "Enable Reading")

### Lấy Telegram Bot Token và Chat ID
1. Tìm @BotFather trên Telegram
2. Gõ lệnh `/newbot` và làm theo hướng dẫn để tạo bot mới
3. Lưu lại token của bot
4. Tìm @userinfobot trên Telegram để lấy Chat ID của bạn

## 5. Lưu ý quan trọng
- Không chia sẻ file `.env` cho người khác
- Nếu nghi ngờ API Key bị lộ, hãy xóa và tạo lại ngay trên Binance
- File `.env` phải được đặt cùng thư mục với file thực thi `.exe` hoặc file chạy Python

## 6. Xử lý lỗi thường gặp
- Nếu bot không chạy, kiểm tra xem đã điền đầy đủ thông tin trong `.env` chưa
- Đảm bảo không có khoảng trắng thừa sau dấu `=`
- Trên Windows, dùng Notepad++ hoặc VS Code để chỉnh sửa file, tránh dùng Notepad vì có thể gây lỗi định dạng

---
📌 **Liên hệ hỗ trợ**: [Điền thông tin liên hệ của bạn]
