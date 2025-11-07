import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

# Load token dan channel dari .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(TOKEN)

# Command /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "👋 Hai! Gunakan perintah:\n\n"
                 "/kirim <pesan>\n\n"
                 "untuk mengirim pesan ke channel dengan tombol link alternatif.")

# Command /kirim
@bot.message_handler(commands=['kirim'])
def kirim_pesan(message):
    try:
        # Ambil teks setelah perintah /kirim
        teks = message.text.split(" ", 1)[1]

        # Buat tombol link
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔗 Link Alternatif 1", url="https://t.me/ClaimEventPajaktoto"),
            InlineKeyboardButton("🔗 Link Alternatif 2", url="https://t.me/fauzanmahjong")
        )

        # Kirim ke channel
        bot.send_message(CHANNEL_ID, teks, reply_markup=markup)
        bot.reply_to(message, "✅ Pesan dengan tombol berhasil dikirim ke channel.")

        print(f"Pesan dikirim: {teks}")

    except IndexError:
        bot.reply_to(message, "⚠️ Format salah. Gunakan:\n/kirim <pesan>")
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi error: {e}")

print("🚀 Bot Telegram siap mengirim ke channel...")
bot.infinity_polling()
