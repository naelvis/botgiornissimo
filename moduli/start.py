import datetime
import telegram.ext
import telegram
import moduli.tokens as tokens
import moduli.smashissimo as smashissimo
import moduli.augurissimi as augurissimi

def start(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    chat_id = update.message.chat_id

    update.message.reply_text("Botgiornissimo è stato attivato. (v1.0).\n Disattivare con /stop.")

    chat_type = context.bot.get_chat(chat_id).type
    if (chat_type != "private"):
        chat_title = context.bot.get_chat(chat_id).title
        context.bot.send_message(tokens.gatto,
                                 "Chat type: {0}\nGroup members: {1}\nGroup title: {2}\nGroup ID: {3}".format(
                                     str(chat_type), str(
                                         context.bot.get_chat_members_count(chat_id) - 1), str(
                                         chat_title), str(chat_id)))
    else:
        chat_title = context.bot.get_chat(chat_id).username
        context.bot.send_message(tokens.gatto,
                                 "Chat type: " + str(chat_type) + "\nUsername: " + str(chat_title) + "\nName: " + str(
                                     context.bot.get_chat(chat_id).first_name) + " " + str(
                                     context.bot.get_chat(chat_id).last_name) + "\nChat ID: " + str(chat_id))

    bg_time = datetime.time(hour=6)  # Enter one hour LESS b/c reasons
    context.job_queue.run_daily(callback=smashissimo.buongiornissimo, time=bg_time, context=chat_id, name="feriale",
                                days=(2,))
    context.job_queue.run_daily(callback=augurissimi.augurissimi, time=bg_time, context=chat_id, name="augurissimi")

    bg_time_weekend = datetime.time(hour=8)  # Enter one hour LESS b/c reasons
    context.job_queue.run_daily(callback=smashissimo.buongiornissimo, time=bg_time_weekend, context=chat_id, name="weekend",
                                days=(5, 6))

    context.job_queue.start()


def stop(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    context.job_queue.stop()

    update.message.reply_text("Botgiornissimo è stato disattivato. (v1.0).\n Riattivare con /start.")

    chat_id = update.message.chat_id
    chat_type = context.bot.get_chat(chat_id).type
    if (chat_type != "private"):
        chat_title = context.bot.get_chat(chat_id).title
        context.bot.send_message(tokens.gatto, "Bot stopped! Chat type: " + str(chat_type) + "\nGroup members: " + str(
            context.bot.get_chat_members_count(chat_id) - 1) + "\nGroup title: " + str(
            chat_title) + "\nGroup ID: " + str(chat_id))
    else:
        chat_title = context.bot.get_chat(chat_id).username
        context.bot.send_message(tokens.gatto, "Bot stopped! Chat type: " + str(chat_type) + "\nUsername: " + str(
            chat_title) + "\nName: " + str(context.bot.get_chat(chat_id).first_name) + " " + str(
            context.bot.get_chat(chat_id).last_name) + "\nChat ID: " + str(chat_id))