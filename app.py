import logging
import os
import random
import re
import time

from telegram import ChatAction
from telegram.ext import Updater, MessageHandler, Filters

RESUME_PATTERN = r"^.*resume template.*\?.*|.*resume example.*\?.*|.*образец resume.*\?.*|.*образец резюме.*\?.*$"
JAVA_PYTHON_PATTERN = r"^.*java or python.*\?.*|.*java или python.*\?.*|.*джав. или питон.*\?.*|.*джав. или пайтон.*\?.*$"
PORTNOV_TESTPRO_PATTERN = r"^.*portnov или.* testpro.*\?.*|.*портнов.* или.* testpro.*\?.*|.*портнов.* или.* тестпро.*\?.*$"
GIF = "https://tenor.com/view/jew-money-invest-gif-24178583"

PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ['WELCOME_BOT_TOKEN']

# with open("token.txt", "r", encoding="utf8") as f:
#     TOKEN = f.read()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def new_member(update, context):
    """ Identifies a new member in a group and sends a welcome message to the member.
    """
    for member in update.message.new_chat_members:
        print(member)
        if member.username:
            user = f"@{member.username}"
        else:
            user = f"{member.first_name} {member.last_name}"

        text = f"Привет, {user}!\nПожалуйста, заполните опросник: \n1. Штат \n2. Текущая " \
               f"должность \n3. Желаемая позиция \n4. Джава или Пайтон?"
        chat_id = update.message.chat.id
        context.bot.send_message(chat_id=chat_id, text=text)


def typing(update, context, chat_id):
    """Emulating real user's typing.
    """
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING, timeout=1)
    time.sleep(0.5)


def resume(update, context):
    """ Parses for resume template queries and replies with a link to a resume example on a GDrive.
    """
    text = "Вот образец резюме (link)"
    chat_id = update.effective_message.chat.id
    message_id = update.effective_message.message_id
    typing(update, context, chat_id)
    context.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=message_id)


def java_python(update, context):
    """ Parses for java vs python holy war and replies with a random image from file.
    """
    path = "images/java_python/"
    random_image = random.choice(os.listdir(path))
    chat_id = update.effective_message.chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(path + random_image, 'rb'))


def portnov_testpro(update, context):
    """ Parses for Portnov vs TestPro query and replies with a related gif.
    """
    chat_id = update.effective_message.chat.id
    context.bot.send_animation(chat_id=chat_id, animation=GIF)


def error(update, context):
    """ Log Errors caused by Updates.
    """
    logger.warning(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    # Add all handlers to the dispatcher and run the bot
    disp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    disp.add_handler(
        MessageHandler(Filters.regex(re.compile(RESUME_PATTERN, re.IGNORECASE)), resume))
    disp.add_handler(
        MessageHandler(Filters.regex(re.compile(JAVA_PYTHON_PATTERN, re.IGNORECASE)), java_python))
    disp.add_handler(
        MessageHandler(Filters.regex(re.compile(PORTNOV_TESTPRO_PATTERN, re.IGNORECASE)),
                       portnov_testpro))
    disp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://menteebot.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == "__main__":
    main()
