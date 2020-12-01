import datetime
import telegram.ext
import telegram
import moduli.tokens as tokens
import moduli.augurissimi as augurissimi
import moduli.smashissimo as smashissimo

REPLY = 1
# First of all, who's asking?

def remote(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    chat_id = update.message.chat_id

    if (chat_id != tokens.gatto):
        return 0
    else:
        update.message.reply_text("Inserire un ID:")
        return REPLY

# Ok, let's see what we can do

def remote_activation(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    chat_id = int(update.message.text)

    context.bot.send_message(update.message.chat_id, text='Attivazione botgiornissimo per ' + str(chat_id))

    if (chat_id == 0):
        return telegram.ext.ConversationHandler.END
    else:
        update.message.reply_text("Botgiornissimo è stato attivato. (v1.0)")

        chat_type = context.bot.get_chat(chat_id).type
        if (chat_type != "private"):
            chat_title = context.bot.get_chat(chat_id).title
        else:
            chat_title = context.bot.get_chat(chat_id).username

        if (chat_type != "private"):
            context.bot.send_message(tokens.gatto,
                                     "Chat type: {0}\nGroup members: {1}\nGroup title: {2}\nGroup ID: {3}".format(
                                         str(chat_type), str(context.bot.get_chat_members_count(chat_id) - 1),
                                         str(chat_title), str(chat_id)))
        else:
            context.bot.send_message(tokens.gatto,
                                     "Chat type: {0}\nUsername: {1}\nName: {2} {3}\nChat ID: {4}".format(
                                         str(chat_type), str(chat_title), str(context.bot.get_chat(chat_id).first_name),
                                         str(context.bot.get_chat(chat_id).last_name), str(chat_id)))
        # weekdays and special
        bg_time = datetime.time(hour=8, minute=0)  # Enter one hour LESS b/c reasons
        context.job_queue.run_daily(callback=smashissimo.buongiornissimo, time=bg_time, context=chat_id, name="feriale",
                                    days=(0, 1, 2, 3, 4))
        context.job_queue.run_daily(callback=augurissimi.augurissimi, time=bg_time, context=chat_id, name="augurissimi")

        # weekend
        bg_time_weekend = datetime.time(hour=8)  # Enter one hour LESS b/c reasons
        context.job_queue.run_daily(callback=smashissimo.buongiornissimo, time=bg_time_weekend, context=chat_id,
                                    name="weekend",
                                    days=(5, 6))

        return telegram.ext.ConversationHandler.END
