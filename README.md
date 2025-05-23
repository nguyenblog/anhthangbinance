# 📊 Binance Crypto Alert Bot

## Giới thiệu

Bot Python tự động quét các cặp coin USDT trên sàn Binance Futures, lọc tín hiệu kỹ thuật (MA, RSI, MACD, volume xanh) và gửi cảnh báo về Telegram. Phù hợp cho trader muốn nhận tín hiệu kỹ thuật nhanh, không cần theo dõi biểu đồ liên tục.

---

## 🚀 Tính năng nổi bật
- Quét dữ liệu thị trường trực tiếp từ Binance
- Tính toán MA, RSI, MACD (DIF/DEA)
- Lọc coin thỏa đồng thời nhiều tiêu chí kỹ thuật
- Gửi cảnh báo về Telegram (rút gọn, đẹp, dễ đọc)
- Hỗ trợ chế độ DEV để test nhanh với coin cụ thể
- Ghi log chi tiết từng coin vào file để debug hoặc kiểm chứng chiến lược
- Cảnh báo Telegram khi có lỗi mạng/API nghiêm trọng

---

## ⚙️ Chiến lược lọc tín hiệu
Một coin sẽ được chọn nếu đồng thời thỏa các điều kiện sau (có thể tùy chỉnh cho từng khung thời gian):

1. **MA ngắn hạn > MA dài hạn** (ví dụ: MA20 > MA50, MA9 > MA21...)
2. **Giá hiện tại > MA ngắn hạn** nhưng không vượt quá MA ngắn hạn + X% (X có thể điều chỉnh)
3. **RSI nằm trong khoảng cho phép** (ví dụ: 55 đến 65)
4. **MACD: DIF > DEA** (tín hiệu tăng ngắn hạn)
5. **Volume xanh liên tiếp** (giá đóng cửa cao hơn nến trước đó, tuỳ cấu hình)

---

## 🧰 Yêu cầu hệ thống
- Python >= 3.8
- Các thư viện trong `requirements.txt` (đã ghi rõ version)

---

## 🔧 Hướng dẫn cài đặt & sử dụng

### 1. Clone mã nguồn & cài thư viện
```bash
git clone <repo này>
cd binance_bot_alert
pip install -r requirements.txt
```

### 2. Tạo file `.env` cấu hình
Sao chép file mẫu `.env.example` (nếu có) hoặc tự tạo `.env` với nội dung như sau:
```env
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
TIME_INTERVAL=60
TIME_INTERVAL_UNIT=minutes
TEST_COINS=BTCUSDT,ETHUSDT
# ...các tham số chiến lược khác (RSI, MA, v.v.)
```
> **Lưu ý:** Không chia sẻ file .env cho người khác!

### 3. Chạy bot cho từng khung thời gian
- Khung 1H: `python main_1h.py`
- Khung 4H: `python main_4h.py`
- Khung 1D: `python main_1d.py`

Bạn có thể chạy nhiều bot song song cho các khung khác nhau.

---

## 📝 Giải thích các tham số cấu hình chính
- `TIME_INTERVAL`, `TIME_INTERVAL_UNIT`: Chu kỳ quét (ví dụ: mỗi 60 phút)
- `TEST_COINS`: Danh sách coin test khi ở chế độ DEV
- `RSI_LOWER_1H`, `RSI_UPPER_1H`, ...: Ngưỡng RSI cho từng khung
- `PRICE_BUFFER_1H`, ...: Ngưỡng giá không vượt quá MA bao nhiêu phần trăm
- `VOLUME_LOOKBACK_1H`, ...: Số nến volume xanh liên tiếp cần kiểm tra

---

## 🔔 Cảnh báo lỗi qua Telegram
- Khi có lỗi mạng hoặc lỗi API Binance, hệ thống sẽ tự động gửi cảnh báo về Telegram (nếu cấu hình đúng BOT TOKEN & CHAT ID).
- Ví dụ cảnh báo: `⚠️ CẢNH BÁO LỖI HỆ THỐNG: Lỗi Binance API khi lấy danh sách symbol...`

---

## ❓ Lỗi thường gặp & cách xử lý
- **Không gửi được tin nhắn Telegram:** Kiểm tra lại BOT TOKEN và CHAT ID trong file .env
- **Lỗi API Binance:** Có thể do key sai, hết hạn, hoặc bị limit request. Kiểm tra log và Telegram để biết chi tiết.
- **ModuleNotFoundError:** Chưa cài đúng thư viện, hãy chạy lại `pip install -r requirements.txt`
- **Lỗi version Python:** Đảm bảo dùng Python >= 3.8

---

## 💡 Gợi ý mở rộng
- Thêm chiến lược hoặc chỉ báo mới (ATR, Bollinger Bands...)
- Gửi báo cáo định kỳ qua Telegram
- Lưu lịch sử tín hiệu vào database hoặc Google Sheets
- Đóng gói chạy Docker hoặc service nền

---

## 📄 Bản quyền & liên hệ
- Tác giả: [Tên bạn/nhóm]
- Liên hệ góp ý: [Telegram/email]
- Mã nguồn mở, sử dụng cho mục đích học tập và cá nhân.
