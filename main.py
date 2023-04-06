import os
import requests
import logging
from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, filters, Application

load_dotenv()

# Telegram Bot API Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! Send me a photo to get started.")


# Define the photo message handler
def photo(update, context):
    # Get the file ID of the photo
    file_id = update.message.photo[-1].file_id

    # Get the file path of the photo
    file_path = context.bot.get_file(file_id).file_path

    # Download the photo from Telegram servers
    photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    response = requests.get(photo_url)
    response.raise_for_status()

    # Process the photo here
    # ...

    # Send the processed photo back to the user
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=response.content)


def main() -> None:
    # # Create the Updater and pass in the bot's token
    # updater = Updater(TOKEN, use_context=True)
    #
    # # Get the dispatcher to register handlers
    # dispatcher = updater.dispatcher
    #
    # # Add the command handler
    # dispatcher.add_handler(CommandHandler("start", start))
    #
    # # Add the photo message handler
    # dispatcher.add_handler(MessageHandler(filters.PHOTO, photo))
    #
    # # Start the bot
    # updater.start_polling()
    #
    # # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    # updater.idle()

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, photo))
    application.run_polling()


if __name__ == '__main__':
    main()
