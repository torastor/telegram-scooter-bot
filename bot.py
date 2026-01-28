import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

SHOP_URL = "https://torastor.github.io/botdragon32.oi/"  
# ⚠️ замени, если repo/username другой

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Открыть магазин",
                web_app=WebAppInfo(url=SHOP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Написать менеджеру",
                url="https://t.me/AgroTech32"
            )
        ]
    ]

    await update.message.reply_text(
        "Добро пожаловать в магазин электроскутеров ⚡\n\n"
        "Выберите модель в каталоге:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
