import re
import time

import telegram
from telegram.ext import Updater, MessageHandler, Filters

RESUME_PATTERN = r"^.*resume template.*\?.*|.*resume example.*\?.*|.*образец resume.*\?.*|.*образец резюме.*\?.*$"

with open("token.txt", "r", encoding="utf8") as f:
    TOKEN = f.read()

updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher


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
    context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING, timeout=1)
    time.sleep(0.5)


def resume(update, context):
    """ Parses for resume template queries and replies with a link to a resume example on a GDrive.
    """
    text = "Вот образец резюме (link)"
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    typing(update, context, chat_id)
    context.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=message_id)


# Add all handlers to the dispatcher and run the bot
disp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
disp.add_handler(MessageHandler(Filters.regex(re.compile(RESUME_PATTERN, re.IGNORECASE)), resume))

updater.start_polling()
updater.idle()
