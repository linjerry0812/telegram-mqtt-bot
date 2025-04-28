import os
import logging
from telegram.ext import Updater, MessageHandler, Filters
import paho.mqtt.publish as publish
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 接下來一樣讀取環境變數
BOT_TOKEN = os.getenv("BOT_TOKEN")
# 其他維持不變

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 讀取環境變數
BOT_TOKEN = os.getenv("BOT_TOKEN")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Debug：確認 BOT_TOKEN 是否讀取成功
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN 沒有正確讀取到！請檢查 Railway 環境變數設定！")
else:
    print(f"✅ BOT_TOKEN 成功讀取: {BOT_TOKEN[:10]}...")

# 當收到訊息時的處理函數
def alert_handler(update, context):
    message = update.message.text
    if any(keyword in message for keyword in ["地震", "規模", "速報"]):
        publish.single(
            MQTT_TOPIC,
            payload="⚠️ 地震速報觸發",
            hostname=MQTT_BROKER,
            port=MQTT_PORT,
            auth={'username': MQTT_USERNAME, 'password': MQTT_PASSWORD},
            tls={'insecure': True}
        )
        logging.info("✅ MQTT 已推送！")

def main():
    # 建立 Telegram Bot，注意這裡顯式指定參數名稱
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # 設定文字訊息處理器
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, alert_handler))

    # 啟動 Bot
    logging.info("🤖 Bot 已啟動，開始監聽訊息...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

