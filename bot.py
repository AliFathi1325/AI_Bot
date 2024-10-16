from g4f.client import Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def AI(prompt):
    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "متاسفانه مشکلی در ارتباط به وجود امده است"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('سلام به ربات هوش مصنوعی خوش اومدی! میتونی سوالت رو بپرسی.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    initial_message = await update.message.reply_text("در حال ایجاد پاسخ...")
    answer = await AI(update.message.text)
    await initial_message.edit_text(answer)
    print(answer)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == '__main__':
    main()
