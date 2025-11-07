import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

# Load token dan channel dari .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(TOKEN)

# Fungsi untuk buat tombol link
def buat_tombol():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔗 Link Alternatif 1", url="https://t.me/ClaimEventPajaktoto"),
        InlineKeyboardButton("🔗 Link Alternatif 2", url="https://t.me/fauzanmahjong")
    )
    return markup

# Command /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "👋 Hai! Gunakan:\n\n"
        "📄 /kirim <pesan> → kirim teks ke channel\n"
        "📸 Kirim gambar langsung → bot akan post ke channel dengan tombol link\n\n"
        "Semua pesan akan otomatis dikirim ke channel yang sudah diatur."
    )

# Command /kirim → kirim teks
@bot.message_handler(commands=['kirim'])
def kirim_teks(message):
    try:
        teks = message.text.split(" ", 1)[1]
        bot.send_message(CHANNEL_ID, teks, reply_markup=buat_tombol())
        bot.reply_to(message, "✅ Pesan teks berhasil dikirim ke channel.")
        print(f"Pesan dikirim: {teks}")
    except IndexError:
        bot.reply_to(message, "⚠️ Format salah. Gunakan:\n/kirim <pesan>")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")
        print(f"Error: {e}")

# Handler untuk pesan foto
@bot.message_handler(content_types=['photo'])
def kirim_foto(message):
    try:
        # Ambil file_id dari foto resolusi tertinggi
        file_id = message.photo[-1].file_id
        caption = message.caption or "(Tidak ada caption)"

        bot.send_photo(CHANNEL_ID, file_id, caption=caption, reply_markup=buat_tombol())
        bot.reply_to(message, "✅ Foto berhasil dikirim ke channel.")
        print(f"Foto dikirim: {caption}")
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi error saat kirim foto: {e}")
        print(f"Error: {e}")

print("🚀 Bot Telegram siap mengirim teks & gambar ke channel...")
bot.infinity_polling()
