import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

# Load token dan channel dari .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Hai! Gunakan perintah:\n\n"
        "/kirim <pesan>\n\n"
        "untuk mengirim pesan ke channel dengan tombol link alternatif."
    )

@bot.message_handler(commands=['kirim'])
def kirim_pesan(message):
    try:
        teks = message.text.split(" ", 1)[1]
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔗 Link Alternatif 1", url="https://t.me/ClaimEventPajaktoto"),
            InlineKeyboardButton("🔗 Link Alternatif 2", url="https://t.me/fauzanmahjong")
        )

        bot.send_message(CHANNEL_ID, teks, reply_markup=markup, parse_mode="HTML")
        bot.reply_to(message, "✅ Pesan dengan tombol berhasil dikirim ke channel.")
        print(f"Pesan dikirim: {teks}")

    except IndexError:
        bot.reply_to(message, "⚠️ Format salah. Gunakan:\n/kirim <pesan>")
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi error: {e}")

print("🚀 Bot Telegram siap mengirim ke channel...")
bot.infinity_polling()
