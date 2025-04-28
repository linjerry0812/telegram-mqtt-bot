import os
import logging
from telegram.ext import Updater, MessageHandler, Filters
import paho.mqtt.publish as publish

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

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
        logging.info("MQTT 已推送！")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, alert_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

