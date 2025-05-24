import requests
import logging
import time
import config

def send_telegram_message(message: str, chat_id: str, bot_token: str):
    """
    Gửi tin nhắn đến Telegram.
    Tích hợp xử lý lỗi Too Many Requests (429).
    """
    if not bot_token or not chat_id:
        logging.error("❌ TOKEN hoặc CHAT_ID Telegram chưa được cấu hình. Không thể gửi tin nhắn.")
        return

    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown" # Sử dụng Markdown để định dạng và link
    }
    
    max_retries = 3 # Số lần thử lại tối đa
    for attempt in range(max_retries):
        try:
            response = requests.post(telegram_api_url, data=payload, timeout=10)
            response.raise_for_status()  # Ném lỗi nếu HTTP request không thành công (4xx hoặc 5xx)
            logging.info("✅ Đã gửi tin nhắn Telegram thành công.")
            return # Gửi thành công, thoát hàm
        except requests.exceptions.HTTPError as e:
            if response is not None and response.status_code == 429:
                try:
                    error_json = response.json() if response.content else {}
                    retry_after = error_json.get("parameters", {}).get("retry_after", 5) # Mặc định 5 giây nếu không có retry_after
                    logging.warning(f"⚠️ Đã đạt giới hạn gửi tin nhắn Telegram (429). Thử lại sau {retry_after} giây...")
                    time.sleep(retry_after + 1) # Chờ thêm 1 giây để an toàn hơn
                except Exception as json_err:
                    logging.error(f"❌ Lỗi khi xử lý phản hồi 429: {json_err}")
                    time.sleep(10)  # Chờ 10 giây nếu không parse được JSON
            else:
                logging.error(f"❌ Lỗi HTTP khi gửi tin nhắn Telegram (Status: {response.status_code}): {e}")
                logging.error(f"Response: {response.text}")
                break # Thoát nếu lỗi không phải 429
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Lỗi mạng khi gửi tin nhắn Telegram: {e}")
            break # Thoát nếu lỗi mạng
        except Exception as e:
            logging.error(f"❌ Lỗi không xác định khi gửi tin nhắn Telegram: {e}")
            break # Thoát nếu lỗi không xác định
    
    logging.error(f"❌ Không thể gửi tin nhắn Telegram sau {max_retries} lần thử.")

def alert_telegram_on_error(error_message: str):
    """
    Gửi cảnh báo lỗi về Telegram (dùng cho toàn bộ hệ thống khi có lỗi mạng hoặc API lớn).
    """
    import config
    try:
        send_telegram_message(f"⚠️ *CẢNH BÁO LỖI HỆ THỐNG*\n{error_message}", config.TELEGRAM_CHAT_ID, config.TELEGRAM_BOT_TOKEN)
    except Exception as e:
        logging.error(f"❌ Không thể gửi alert Telegram khi gặp lỗi: {e}")