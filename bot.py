import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

# Load file .env
load_dotenv()

# Ambil token & channel dari .env
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN:
    raise ValueError("❌ TOKEN tidak ditemukan. Pastikan file .env sudah benar.")
if not CHANNEL_ID:
    raise ValueError("❌ CHANNEL_ID tidak ditemukan. Pastikan file .env sudah benar.")

bot = telebot.TeleBot(TOKEN)

# Command /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "👋 Hai! Sekarang bot bisa kirim:\n\n"
        "📸 Gambar yang kamu kirim langsung\n"
        "🖼️ Gambar dari URL\n"
        "📝 Pesan teks biasa\n\n"
        "Gunakan:\n"
        "• /kirim <pesan>\n"
        "• /kirim <url_gambar> | <caption>\n"
        "Atau cukup kirim gambar langsung (dengan caption optional)."
    )

# Command /kirim untuk teks / gambar dari URL
@bot.message_handler(commands=['kirim'])
def kirim_pesan(message):
    try:
        teks = message.text.split(" ", 1)[1]

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔗 Link Alternatif 1", url="https://t.me/ClaimEventPajaktoto"),
            InlineKeyboardButton("🔗 Link Alternatif 2", url="https://t.me/fauzanmahjong")
        )

        # Jika berisi link gambar
        if "|" in teks:
            link_gambar, caption = teks.split("|", 1)
            link_gambar = link_gambar.strip()
            caption = caption.strip()
            bot.send_photo(CHANNEL_ID, link_gambar, caption=caption, reply_markup=markup)
        elif teks.startswith("http") and (".jpg" in teks or ".png" in teks or ".jpeg" in teks):
            bot.send_photo(CHANNEL_ID, teks, caption="📸 Gambar baru!", reply_markup=markup)
        else:
            bot.send_message(CHANNEL_ID, teks, reply_markup=markup)

        bot.reply_to(message, "✅ Pesan berhasil dikirim ke channel.")
        print(f"Pesan dikirim: {teks}")

    except IndexError:
        bot.reply_to(message, "⚠️ Format salah. Gunakan:\n/kirim <pesan>\natau\n/kirim <url_gambar> | <caption>")
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi error: {e}")
        print(f"Error: {e}")

# 🖼️ Jika user kirim foto langsung
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        caption = message.caption if message.caption else "📸 Foto dari admin."
        photo_id = message.photo[-1].file_id  # ambil resolusi terbaik

        # Buat tombol link
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔗 Link Alternatif 1", url="https://t.me/ClaimEventPajaktoto"),
            InlineKeyboardButton("🔗 Link Alternatif 2", url="https://t.me/fauzanmahjong")
        )

        # Kirim foto ke channel
        bot.send_photo(CHANNEL_ID, photo_id, caption=caption, reply_markup=markup)
        bot.reply_to(message, "✅ Gambar berhasil dikirim ke channel.")
        print(f"Foto dikirim ke {CHANNEL_ID} | Caption: {caption}")

    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi error saat kirim gambar: {e}")
        print(f"Error kirim gambar: {e}")

print("🚀 Bot Telegram siap mengirim gambar & pesan ke channel...")
bot.infinity_polling()
