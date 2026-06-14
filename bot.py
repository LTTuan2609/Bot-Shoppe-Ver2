import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFF_ID = os.getenv("AFF_ID")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if "shopee" not in text and "shp.ee" not in text:
        await update.message.reply_text(
            "Vui lòng gửi link Shopee."
        )
        return

    try:

        response = requests.get(
            "https://addlivetag.com/short-link.php",
            params={
                "aff_id": AFF_ID,
                "url": text
            },
            headers={
                "X-Requested-With": "XMLHttpRequest"
            },
            timeout=30
        )

        data = response.json()

        if data.get("success"):

            await update.message.reply_text(
                data["affiliateLink"]
            )

        else:

            await update.message.reply_text(
                "Không tạo được link affiliate."
            )

    except Exception as e:

        await update.message.reply_text(
            f"Lỗi: {e}"
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

app.run_polling()