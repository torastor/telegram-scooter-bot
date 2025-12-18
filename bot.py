import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8357035866:AAHIJdY2r0J-OY3I24W05Z__AaPFx_KKr0s"

MODELS = [
    {
        "name": "Fududu A5",
        "price": 78000,
        "place": ["город", "бездорожье"],
        "range": 100,
        "weight": 200,
        "folding": False,
        "link": "https://t.me/AgroTech32/409"
    },
    {
        "name": "Fududu A1",
        "price": 55000,
        "place": ["город", "бездорожье"],
        "range": 40,
        "weight": 150,
        "folding": False,
        "link": "https://t.me/AgroTech32/407"
    },
    {
        "name": "Fududu C1",
        "price": 30000,
        "place": ["город"],
        "range": 25,
        "weight": 100,
        "folding": True,
        "link": "https://t.me/AgroTech32/286"
    },
    {
        "name": "FUDUDU B1",
        "price": 48000,
        "place": ["город"],
        "range": 40,
        "weight": 150,
        "folding": False,
        "link": "https://t.me/AgroTech32/410"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 До 40 000 ₽", callback_data="budget_40000")],
        [InlineKeyboardButton("💰 До 60 000 ₽", callback_data="budget_60000")],
        [InlineKeyboardButton("💰 До 100 000 ₽", callback_data="budget_100000")]
    ]
    await update.message.reply_text(
        "Привет! Я помогу подобрать электроскутер 🚲\nВыбери бюджет:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("budget"):
        context.user_data["budget"] = int(data.split("_")[1])
        keyboard = [
            [InlineKeyboardButton("🏙 Город", callback_data="place_город")],
            [InlineKeyboardButton("🌲 Бездорожье", callback_data="place_бездорожье")]
        ]
        await query.message.reply_text(
            "Где планируете ездить?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("place"):
        context.user_data["place"] = data.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("25 км", callback_data="range_25")],
            [InlineKeyboardButton("40 км", callback_data="range_40")],
            [InlineKeyboardButton("100 км", callback_data="range_100")]
        ]
        await query.message.reply_text(
            "Какая дальность маршрута?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("range"):
        context.user_data["range"] = int(data.split("_")[1])
        keyboard = [
            [InlineKeyboardButton("До 100 кг", callback_data="weight_100")],
            [InlineKeyboardButton("До 150 кг", callback_data="weight_150")],
            [InlineKeyboardButton("До 200 кг", callback_data="weight_200")]
        ]
        await query.message.reply_text(
            "Какая грузоподъёмность нужна?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("weight"):
        context.user_data["weight"] = int(data.split("_")[1])
        keyboard = [
            [InlineKeyboardButton("Да", callback_data="folding_yes")],
            [InlineKeyboardButton("Нет", callback_data="folding_no")]
        ]
        await query.message.reply_text(
            "Нужна складная модель?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("folding"):
        context.user_data["folding"] = data.endswith("yes")

        result = None
        for model in MODELS:
            if (
                model["price"] <= context.user_data["budget"]
                and context.user_data["place"] in model["place"]
                and model["range"] >= context.user_data["range"]
                and model["weight"] >= context.user_data["weight"]
                and model["folding"] == context.user_data["folding"]
            ):
                result = model
                break

        if result:
            keyboard = [[InlineKeyboardButton("🔎 Подробнее", url=result["link"])]]
            await query.message.reply_text(
                f"✅ Подходящая модель:\n\n"
                f"{result['name']}\n"
                f"Цена: {result['price']} ₽\n"
                f"Дальность: {result['range']} км\n"
                f"Грузоподъёмность: {result['weight']} кг",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.message.reply_text(
                "😕 К сожалению, точного совпадения не найдено.\n"
                "Напишите менеджеру — мы подберём лучший вариант."
            )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()

