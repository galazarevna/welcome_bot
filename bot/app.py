from telegram.ext import Updater, MessageHandler, Filters

with open("token.txt", "r", encoding="utf8") as f:
    TOKEN = f.read()

updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher


def new_member(update, context):
    """ Identifies a new member in a grouup and sends a welcome message to the member.
    """
    for member in update.message.new_chat_members:
        print(member)
        if member.username:
            user = f"@{member.username}"
        else:
            user = f"{member.first_name} {member.last_name}"

        text = f"Привет, {user}!\nПожалуйста, заполните опросник: \n1. Штат \n2. Текущая " \
               f"должность \n3. Желаемая позиция \n4. Джава или Пайтон? "
        chat_id = update.message.chat.id
        context.bot.send_message(chat_id=chat_id, text=text)


disp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

updater.start_polling()
updater.idle()
