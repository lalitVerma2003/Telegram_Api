import os
import django
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_assignment.settings')
django.setup()

from users.models import User
from config.environment import TELEGRAM_BOT_TOKEN

from asgiref.sync import sync_to_async

logging.basicConfig(level=logging.INFO)

@sync_to_async
def get_or_create_user(user_data):
    return User.objects.get_or_create(
        telegram_id=user_data.id,
        defaults={
            "fullname": f"{user_data.first_name} {user_data.last_name}"
        }
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await get_or_create_user(user)

    await update.message.reply_text(f"Welcome, {user.first_name} {user.last_name}!")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()  # or run_webhook()

if __name__ == '__main__':
    main()
