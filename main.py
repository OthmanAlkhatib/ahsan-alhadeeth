from telegram.ext import CommandHandler, Updater, ConversationHandler, MessageHandler, Filters, CallbackContext
from telegram import (KeyboardButton, ReplyKeyboardMarkup, Update)
# from dataSource import DataSource
import os
# import threading
# import time
# import datetime
import logging
import sys


READER_DATA = {
    "أنس بادي":
        {
            "سورة الكهف كاملة": "https://t.me/ahsan_alhadeeth/75"
        },
    "الشيخ محمد المصري":
       {
           "مقتطف من سورة الصافات": "https://t.me/ahsan_alhadeeth/104",
           "مقتطف من سورة الأنعام": "https://t.me/ahsan_alhadeeth/67"
        }
}

Readers = list(READER_DATA.keys())
BACK_BUTTON = "رجوع"

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")

MODE = os.getenv("MODE")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if MODE == "dev":
    def run():
        logger.info("Start in DEV mode")
        updater.start_polling()
elif MODE == "prod":
    def run():
        logger.info("Start in PROD mode")
        updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), url_path=TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format("ahsan-alhadeeth", TOKEN))
else:
    logger.error("No mode specified")
    sys.exit(1)

def start_handler(update, context):
    # Reply With Next Step (Buttons)
    update.message.reply_text("حياك الله في قناة أحسن الحديث, الرجاء اختيار قارئ", reply_markup=reader_buttons())

def back(update: Update, context: CallbackContext):
    update

def reader_info(reader):
    return list(READER_DATA[reader].keys())


def reader_buttons():
    # Storing Buttons (Rows and Columns)
    keyboard = [[KeyboardButton(i)] for i in list(READER_DATA.keys())]
    return ReplyKeyboardMarkup(keyboard)

def reader_video_buttons(update: Update, context: CallbackContext) :
    # Storing Buttons (Rows and Columns)
    message = update.message.text
    reader = reader_info(message)
    context.user_data["reader_name"] = message

    keyboard = [[KeyboardButton(reader[i])] for i in range(len(reader))]
    keyboard.append([KeyboardButton(BACK_BUTTON)])
    update.message.reply_text("اختر تلاوة", reply_markup=ReplyKeyboardMarkup(keyboard))



def reader_video_button_handler(update: Update, context: CallbackContext) :
    reader_name = context.user_data["reader_name"]
    telawa = update.message.text
    update.message.bot.send_video(update.message.chat_id, READER_DATA[reader_name][telawa])

def choose_telawa(update: Update, context: CallbackContext):
    update.message.reply_text("اختر تلاوة", reply_markup=reader_video_buttons)

if __name__ == "__main__":
    # Activate Bot
    updater = Updater(TOKEN, use_context=True)
    # Add Command Handler (Which Function Will Be Called When Using Exact Command)
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))

    for reader in Readers:
        updater.dispatcher.add_handler(MessageHandler(Filters.text(reader), reader_video_buttons))

    for reader in Readers:
        reader_telawat = list(READER_DATA[reader].keys())
        for telawa in reader_telawat:
            updater.dispatcher.add_handler(
                MessageHandler(Filters.text(telawa), reader_video_button_handler))

    updater.dispatcher.add_handler(MessageHandler(Filters.text(BACK_BUTTON), start_handler))

    run()
