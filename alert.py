import requests
import logging
import time
import config

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    WebClient = None
    SlackApiError = None

def send_slack_message(message: str):
    """
    Gửi tin nhắn tới Slack nếu có cấu hình token và channel.
    """
    slack_token = getattr(config, "SLACK_TOKEN", None)
    slack_channel = getattr(config, "SLACK_CHANNEL_ID", None)
    if not slack_token or not slack_channel:
        logging.error("❌ SLACK_TOKEN hoặc SLACK_CHANNEL_ID chưa được cấu hình. Không thể gửi tin nhắn Slack.")
        return
    if WebClient is None:
        logging.error("❌ slack_sdk chưa được cài đặt. Không thể gửi tin nhắn Slack.")
        return
    try:
        client = WebClient(token=slack_token)
        response = client.chat_postMessage(channel=slack_channel, text=message)
        logging.info(f"Đã gửi tin nhắn Slack: {response['ts']}")
    except SlackApiError as e:
        logging.error(f"❌ Lỗi gửi Slack: {e.response['error']}")
    except Exception as e:
        logging.error(f"❌ Lỗi không xác định khi gửi Slack: {e}")

def send_telegram_message(message: str, chat_id: str = None, bot_token: str = None):
    """
    Gửi tin nhắn đến Slack (bỏ qua Telegram).
    """
    send_slack_message(message)


def alert_telegram_on_error(error_message: str):
    """
    Gửi cảnh báo lỗi về Slack (bỏ qua Telegram hoàn toàn).
    """
    send_slack_message(f"⚠️ *CẢNH BÁO LỖI HỆ THỐNG*\n{error_message}")