# Hướng dẫn tạo tài khoản Slack, thêm bot vào channel và lấy Slack Token, Channel ID

## 1. Đăng ký tài khoản và tạo workspace Slack

1. Truy cập [https://slack.com/get-started](https://slack.com/get-started)
2. Chọn **Create a new workspace**.
3. Nhập email, xác nhận mã gửi về email.
4. Đặt tên workspace và channel đầu tiên (ví dụ: `alerts`).

---

## 2. Tạo Slack App (Bot)

1. Vào [https://api.slack.com/apps](https://api.slack.com/apps)
2. Bấm **Create New App** > **From scratch**.
3. Đặt tên cho app (ví dụ: `Binance Alert Bot`), chọn workspace vừa tạo.
4. Sau khi tạo xong, vào phần **OAuth & Permissions** (bên trái).

---

## 3. Cấp quyền cho Bot

1. Trong mục **OAuth & Permissions**, kéo xuống phần **Bot Token Scopes**.
2. Thêm các quyền sau:
   - `chat:write` (bắt buộc, để bot gửi tin nhắn)
   - `channels:read` (để bot đọc danh sách channel)
3. Bấm **Save Changes**.

---

## 4. Cài bot vào workspace và lấy Bot Token

1. Vẫn ở trang Slack App, vào mục **OAuth & Permissions**.
2. Bấm **Install App to Workspace** (hoặc **Reinstall to Workspace** nếu đã từng cài).
3. Chọn **Allow** để cài bot.
4. Sau khi cài xong, bạn sẽ thấy dòng **Bot User OAuth Token** dạng:
   ```
   xoxb-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
   ```
   => Đây chính là **SLACK_TOKEN**.

---

## 5. Thêm bot vào channel

1. Vào Slack, chọn channel bạn muốn nhận thông báo (ví dụ: #alerts).
2. Gõ lệnh:
   ```
   /invite @TênBot
   ```
   (TênBot là tên bạn đặt khi tạo app, ví dụ: Binance Alert Bot)

---

## 6. Lấy Channel ID

1. Mở channel trên Slack (trên web).
2. Nhìn lên thanh địa chỉ trình duyệt, bạn sẽ thấy đường link dạng:
   ```
   https://app.slack.com/client/Txxxxxxx/C08TZ10JLG5
   ```
   - Phần **C08TZ10JLG5** chính là **SLACK_CHANNEL_ID**.

---

## 7. Điền vào file .env

```env
SLACK_TOKEN=xoxb-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_CHANNEL_ID=C08TZ10JLG5
```

---

## 8. Kiểm tra

- Chạy bot, nếu cấu hình đúng, bot sẽ gửi tin nhắn vào channel đã chọn.

---

### Lưu ý

- Nếu đổi channel, cần lấy lại Channel ID mới.
- Nếu đổi workspace, cần cài lại bot vào workspace mới.
- Không chia sẻ SLACK_TOKEN cho người khác.

---

Nếu cần hướng dẫn chi tiết hơn hoặc gặp lỗi, hãy liên hệ hỗ trợ!
