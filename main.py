from telegram.ext import CommandHandler, Updater, ConversationHandler, MessageHandler, Filters, CallbackContext
from telegram import (KeyboardButton, ReplyKeyboardMarkup, Update)
from dataSource import DataSource
import os
import logging
import sys


READER_DATA = {
    "القارئ أنس بادي":
        {
            "سورة الكهف كاملة": ["https://t.me/ahsan_alhadeeth/75", "https://t.me/ahsan_alhadeeth/76"],
            "سورة الملك كاملة": ["https://t.me/ahsan_alhadeeth/39", "https://t.me/ahsan_alhadeeth/40"],
            "سورة الإنسان كاملة": ["https://t.me/mstoda3/120", "https://t.me/mstoda3/121"],
            "دعاء رمضان 1442": ["https://t.me/mstoda3/98", "https://t.me/mstoda3/99"],
            "من سورة لقمان": ["https://t.me/mstoda3/91", "https://t.me/mstoda3/92"],
        },
    "الشيخ محمد المصري":
       {
            "من سورة الصافات": ["https://t.me/mstoda3/126", "https://t.me/mstoda3/124"],
            "من سورة الأنعام 2": ["https://t.me/ahsan_alhadeeth/67", "https://t.me/ahsan_alhadeeth/68"],
            "من سورة ص" : ["https://t.me/ahsan_alhadeeth/33","https://t.me/ahsan_alhadeeth/34"],
            "من سورة الأحزاب" : ["https://t.me/mstoda3/117","https://t.me/mstoda3/118"],
            "من سورة الإسراء" : ["https://t.me/mstoda3/105","https://t.me/mstoda3/106"],
            "من سورة الرعد" : ["https://t.me/mstoda3/85","https://t.me/mstoda3/86"],
            "من سورة الأعراف" : ["https://t.me/mstoda3/70","https://t.me/mstoda3/73"],
            "من سورة الأنعام": ["https://t.me/mstoda3/59", "https://t.me/mstoda3/75"],
        },
    "القارئ خالد جيزاوي":
        {
            "سورة الطور كاملة": ["https://t.me/mstoda3/128", "https://t.me/mstoda3/139"],
            "من سورة الواقعة": ["https://t.me/ahsan_alhadeeth/62", "https://t.me/ahsan_alhadeeth/63"],
            "من سورة الفرقان": ["https://t.me/ahsan_alhadeeth/20", "https://t.me/ahsan_alhadeeth/21"],
        },
    "القارئ عدنان الجودي":
        {
            "من سورة البقرة": ["https://t.me/ahsan_alhadeeth/83", "https://t.me/ahsan_alhadeeth/84"],
            "من سورة آل عمران": ["https://t.me/ahsan_alhadeeth/42", "https://t.me/ahsan_alhadeeth/43"],
            "من سورة الإسراء": ["https://t.me/mstoda3/114", "https://t.me/mstoda3/115"],
            "من سورة ابراهيم": ["https://t.me/mstoda3/101", "https://t.me/mstoda3/102"],
        },
    "الشيخ محمد أنس علوش":
        {
            "من سورة مريم": ["https://t.me/mstoda3/127", "https://t.me/mstoda3/125"],
            "من سورة الحجرات": ["https://t.me/mstoda3/108", "https://t.me/mstoda3/109"],
            "من سورة القصص": ["https://t.me/mstoda3/88", "https://t.me/mstoda3/89"],
            "من سورة النمل": ["https://t.me/mstoda3/79", "https://t.me/mstoda3/80"],
            "من سورة طه": ["https://t.me/mstoda3/63", "https://t.me/mstoda3/76"],
        },
    "الشيخ صفوح الكيلاني":
        {
            "من سورة يونس": ["https://t.me/mstoda3/147", "https://t.me/mstoda3/148"],
            "من سورة يس": ["https://t.me/ahsan_alhadeeth/28", "https://t.me/ahsan_alhadeeth/29"],
            "سورة المنافقون كاملة": ["https://t.me/mstoda3/111", "https://t.me/mstoda3/112"],
            "من سورة مريم": ["https://t.me/mstoda3/95", "https://t.me/mstoda3/96"],
            "من سورة يوسف": ["https://t.me/mstoda3/82", "https://t.me/mstoda3/83"],
        },
    "الشيخ محمود مطر":
        {
            "من سورة ابراهيم": ["https://t.me/mstoda3/149", "https://t.me/mstoda3/150"],
            "من سورة المؤمنون": ["https://t.me/ahsan_alhadeeth/93", "https://t.me/ahsan_alhadeeth/94"],
            "من سورة طه": ["https://t.me/ahsan_alhadeeth/47", "https://t.me/ahsan_alhadeeth/48"],
            "من سورة مريم": ["https://t.me/ahsan_alhadeeth/11", "https://t.me/ahsan_alhadeeth/13"],
        },
    "القارئ نبراس العبدالله":
        {
            "من سورة الصافات": ["https://t.me/ahsan_alhadeeth/71", "https://t.me/ahsan_alhadeeth/72"],
            "من سورة القصص": ["https://t.me/ahsan_alhadeeth/16", "https://t.me/ahsan_alhadeeth/17"],
        },
    "الشيخ نادر الدباغ":
        {
            "سورة ق كاملة": ["https://t.me/mstoda3/151", "https://t.me/mstoda3/152"],
            "من سورة القصص": ["https://t.me/ahsan_alhadeeth/99", "https://t.me/ahsan_alhadeeth/100"],
            "من سورة الأنبياء": ["https://t.me/ahsan_alhadeeth/51", "https://t.me/ahsan_alhadeeth/52"],
            "من سورة مريم": ["https://t.me/ahsan_alhadeeth/24", "https://t.me/ahsan_alhadeeth/25"],
        }
}

Readers = list(READER_DATA.keys())
BACK_BUTTON = "رجوع"

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")

MODE = os.getenv("MODE")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

data_source = DataSource(DATABASE_URL)
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
    update.message.reply_text("""
    حياك الله في بوت قناة أحسن الحديث ❤️
    
    لا تنسَ الاشتراك في قناتنا الرسمية على تلغرام عبر الرابط التالي : https://t.me/ahsan_alhadeeth
    لتبقى على اطلاع بأحدث المنشورات والتلاوات العطرة في القناة

    """)
    update.message.reply_text("الرجاء اختيار قارئ", reply_markup=reader_buttons())
    data_source.add_user()

def goBack(update: Update, context: CallbackContext):
    update.message.reply_text("الرجاء اختيار قارئ", reply_markup=reader_buttons())

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
    update.message.bot.send_video(update.message.chat_id, READER_DATA[reader_name][telawa][0])
    update.message.bot.send_video(update.message.chat_id, READER_DATA[reader_name][telawa][1])


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

    updater.dispatcher.add_handler(MessageHandler(Filters.text(BACK_BUTTON), goBack))

    data_source.create_tables()
    run()
