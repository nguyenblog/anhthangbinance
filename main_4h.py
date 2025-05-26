import datetime
import pandas as pd
import logging
import pytz
import time
import schedule
import sys 

from binance.client import Client
from strategy import check_conditions_4h as check_conditions, format_telegram_message 
from alert import send_telegram_message
from data import get_all_symbols, get_klines
from indicators import add_all_indicators
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Chu kỳ chạy bot riêng cho 4H
TIME_INTERVAL = config.TIME_INTERVAL_4H
TIME_INTERVAL_UNIT = config.TIME_INTERVAL_UNIT_4H

def run_strategy_4h(): 
    logging.info("=========== Bắt đầu chu kỳ quét 4H ===========")
    client = Client(api_key=config.BINANCE_API_KEY, api_secret=config.BINANCE_API_SECRET) 

    if config.IS_DEV and config.TEST_COINS:
        tickers = config.TEST_COINS.split(",")
        logging.info(f"[DEV MODE] Kiểm tra coin test: {tickers}")
    else:
        tickers = get_all_symbols()
        logging.info(f"[PROD MODE] Tổng số coin: {len(tickers)}")

    total = len(tickers)
    scanned = 0
    matched = 0

    # Chia danh sách coin thành các batch 30 coin
    batch_size = 30
    for batch_start in range(0, total, batch_size):
        batch = tickers[batch_start:batch_start+batch_size]
        matched_coins_info = []
        for symbol in batch:
            try:
                scanned += 1
                logging.info(f"🔍 Đang kiểm tra {symbol} … ({scanned}/{total})")

                df = get_klines(
                    symbol=symbol,
                    interval=config.CANDLE_INTERVAL_4H, 
                    limit=config.CANDLE_LIMIT
                )
                
                required_klines = max(20, 50, 26) + config.VOLUME_LOOKBACK_4H + 1 
                if len(df) < required_klines: 
                    logging.warning(f"⚠️ {symbol}: Không đủ dữ liệu nến ({len(df)} < {required_klines}) để tính toán chỉ báo. Bỏ qua.")
                    continue

                df = add_all_indicators(df, short=20, long=50) 
                result, passed, extra = check_conditions(df) 

                if config.IS_DEV:
                    if len(df) >= required_klines:
                        local_time = df.index[-2].tz_localize("UTC").astimezone(pytz.timezone("Asia/Ho_Chi_Minh"))
                        volume_debug_str = []
                        sorted_volume_info = sorted(extra["volume_color_info"], key=lambda x: x['idx'], reverse=True)
                        for vol_info in sorted_volume_info:
                            current_idx = vol_info['idx']
                            vol_val = vol_info['volume']
                            is_gv = vol_info['is_green_volume']
                            volume_debug_str.append(f"Idx {current_idx}: {vol_val:.2f} {'(Xanh)' if is_gv else '(Đỏ)'}")
                        volume_debug_output = ", ".join(volume_debug_str)
                        print(f"\n🔍 {symbol}")
                        print(f"⏳ Dữ liệu đến: {local_time.strftime('%Y-%m-%d %H:%M:%S')} (Asia/Ho_Chi_Minh)")
                        print(f"Giá: {extra['price']:.6f} | MA20: {extra['ma_short']:.6f} | MA50: {extra['ma_long']:.6f}") 
                        print(f"RSI: {extra['rsi']:.2f} | DIF: {extra['dif']:.6f} | DEA: {extra['dea']:.6f}")
                        print(f"Volume hiện tại: {extra['volume_now']:.2f} | Volume {config.VOLUME_LOOKBACK_4H} nến gần nhất: {volume_debug_output}")
                        for k, v in result.items():
                            print(f"   ✅ {k}: {'✔️' if v else '❌'}")
                    else:
                        print(f"⚠️ Không đủ dữ liệu cho {symbol} để hiển thị debug (ít hơn {required_klines} nến).")

                if passed:
                    matched += 1
                    extra["symbol"] = symbol
                    message = format_telegram_message([extra], timeframe="4H")
                    send_telegram_message(message, config.TELEGRAM_CHAT_ID, config.TELEGRAM_BOT_TOKEN)

            except Exception as e:
                logging.error(f"❌ Lỗi khi xử lý {symbol}: {e}", exc_info=config.IS_DEV)
        # Sau mỗi batch 30 coin, nghỉ 1 giây
        if matched_coins_info:
            message = format_telegram_message(matched_coins_info, timeframe="4H")
            send_telegram_message(message, config.TELEGRAM_CHAT_ID, config.TELEGRAM_BOT_TOKEN)
        time.sleep(1)

    if matched == 0:
        send_telegram_message("❗[4H] Không có đồng coin nào thỏa điều kiện.") 

    summary = f"📊 Tổng kết [4H]:\n🔍 Đã kiểm tra {scanned}/{total} coin.\n✅ Có {matched} coin thỏa tất cả điều kiện." 
    send_telegram_message(summary)
    print("\n" + summary)
    logging.info("=========== Kết thúc chu kỳ quét 4H ===========\n")

if __name__ == "__main__":
    logging.info(f"Bot khởi động cho khung 4H.")
    
    if TIME_INTERVAL_UNIT == "minutes":
        schedule.every(TIME_INTERVAL).minutes.do(run_strategy_4h)
        logging.info(f"Bot 4H sẽ chạy mỗi {TIME_INTERVAL} phút.")
    elif TIME_INTERVAL_UNIT == "hours":
        schedule.every(TIME_INTERVAL).hours.do(run_strategy_4h)
        logging.info(f"Bot 4H sẽ chạy mỗi {TIME_INTERVAL} giờ.")
    else:
        logging.error("Đơn vị thời gian không hợp lệ. Vui lòng kiểm tra TIME_INTERVAL_UNIT_4H trong .env")
        exit()

    run_strategy_4h() 

    print("\n") 

    while True:
        schedule.run_pending()
        
        next_run_time = schedule.next_run()
        if next_run_time:
            time_until_next_run = (next_run_time - datetime.datetime.now()).total_seconds()
            
            if time_until_next_run > 0:
                mins, secs = divmod(int(time_until_next_run), 60)
                hours, mins = divmod(mins, 60)
                sys.stdout.write(f"\r⏳ Chu kỳ tiếp theo sau: {hours:02d} giờ {mins:02d} phút {secs:02d} giây ")
                sys.stdout.flush()
            else:
                sys.stdout.write("\r✨ Đang khởi chạy chu kỳ mới...                           ")
                sys.stdout.flush()
                print("\n") 
        else:
            sys.stdout.write("\rĐang chờ chu kỳ tiếp theo được lên lịch...             ")
            sys.stdout.flush()
        
        time.sleep(1)