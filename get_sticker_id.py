import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


from telegram.ext import Application, MessageHandler, filters, ContextTypes


async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    await update.message.reply_text(f"Sticker ID: {sticker.file_id}")
    print(f"Received sticker: {sticker.file_id}")


app = Application.builder().token("7722655180:AAHmAhYvwVBZ_-H5CBHw6FONEPc4ggCCXIg").build()
app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
app.run_polling()
