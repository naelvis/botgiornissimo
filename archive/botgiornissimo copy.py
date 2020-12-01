# -*- coding: utf-8 -*-
"""
# v0.4
"""

import datetime
import github
import random

import logging

from telegram import (
#    Poll,
#    ParseMode,
#    KeyboardButton,
#    KeyboardButtonPollType,
#    ReplyKeyboardMarkup,
#    ReplyKeyboardRemove,
    Update
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    PollAnswerHandler,
#    PollHandler,
    MessageHandler,
    Filters
)

g = github.Github("339137eee6e19d27e109a98c721f0920ba340e62")
repo = g.get_user().get_repo("botgiornissimo")
# print(repo)

# print(bot.get_me())

# Enable logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

chat_id_int = 61300195

def start(update: Update, context: CallbackContext) -> None:
    
    if(update.message.chat_id == 61300195):
        chat_id = -1001254499375
        #chat_id = 61300195
    else:
        chat_id = update.message.chat_id
    
    update.message.reply_text("Botgiornissimo è stato attivato. (v0.5)")
    
    chat_type = context.bot.get_chat(chat_id).type
    if (chat_type != "private"):
        chat_title = context.bot.get_chat(chat_id).title
    else:
        chat_title = context.bot.get_chat(chat_id).username
    
    if (chat_type != "private"):
        context.bot.send_message(chat_id_int, "Chat type: " + str(chat_type) + "\nGroup members: " + str(context.bot.get_chat_members_count(chat_id) - 1) + "\nGroup title: " + str(chat_title) + "\nGroup ID: " + str(chat_id))
    else:
        context.bot.send_message(chat_id_int, "Chat type: " + str(chat_type) + "\nUsername: " + str(chat_title) + "\nName: " + str(context.bot.get_chat(chat_id).first_name) + " " + str(context.bot.get_chat(chat_id).last_name) + "\nChat ID: " + str(chat_id))

    bg_time = datetime.time(hour = 6) #Enter one hour LESS b/c reasons
    
    context.job_queue.run_daily(callback=buongiornissimo, time=bg_time, context=chat_id, name=str(chat_id), days = (0, 1, 2, 3, 4))
    
    bg_time_weekend = datetime.time(hour = 8) #Enter one hour LESS b/c reasons
    
    context.job_queue.run_daily(callback=buongiornissimo, time=bg_time_weekend, context=chat_id, name=str(chat_id) + "_weekend", days = (5, 6))
    
    # Debugging
    #jobDay = context.job_queue.run_daily(callback=pictures, time=bg_time, context=chat_id, name=str(chat_id))
    #jobRepeating = context.job_queue.run_repeating(pictures, 10)
    #print(jobDay.next_t)
    #print(jobRepeating.next_t)

    
def buongiornissimo(context: CallbackContext) -> None:
    """Send the pictures message."""
    job = context.job
    
    #context.bot.send_message(job.context, text='Beep!')
    
    images = list(map(lambda x : x.path, repo.get_contents("pictures")))
    urls = list(map(lambda x: "https://raw.githubusercontent.com/naelvis/botgiornissimo/master/" + x, [x for x in images if not(x.endswith("Store"))]))
    names = list(map(lambda x : x[16:100], [x for x in images if not(x.endswith("Store"))]))
    image_dict = dict(zip(names, urls))
        
    weekday = datetime.datetime.now().weekday()
    
    if (weekday == 0) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("LU") | key.startswith("X"))}
    elif (weekday == 1) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("MA") | key.startswith("X"))}
    elif (weekday == 2) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("Mitt"))}
    elif (weekday == 3) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("GI") | key.startswith("X"))}
    elif (weekday == 4) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("VE") | key.startswith("X"))}
    elif (weekday == 5) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("SA") | key.startswith("X"))}
    elif (weekday == 6) :
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("DO") | key.startswith("X"))}
                
    image = random.choice(list(dict_subset.values()))
            
    if (weekday == 2):
        bg_message = "Es ist Mittwoch, meine Kerle!"
    else:
        bg_message = random.choice(["Buongiornissimo!", "Caffèèèèèè?", "Stamattina non si saluta?", "Buongiornissimo amici!", "Ecco il caffè!", "Caffè a tutti e si parte!"])
        
        
    context.bot.send_photo(job.context,
                           photo=image,
                           caption = bg_message)
            
    if (weekday == 3 and context.bot.get_chat(job.context).type != "private"):
        alternative = ["Venerdì alle 21", "Sabato alle 21", "No", "Altro (specificare)"]
        
        smashissimo = context.bot.send_poll(job.context, 
                      question="Smashissimo questa settimana?",
                      options = alternative,
                      is_anonymous = False,
                      allows_multiple_answers = True)
        
        payload = {
        smashissimo.poll.id: {
            "questions": alternative,
            "message_id": smashissimo.message_id,
            "chat_id": job.context,
            "answers": 0,
            "results": dict(),
        }
        }
        
        context.bot_data.update(payload)
        

def update_poll_results(poll, options, x):
    
    poll[options[x]] = poll.setdefault(options[x], 0) + 1
    return(poll)
  

def smashissimo_quando(update: Update, context: CallbackContext) -> None:
    """Communicates smashissimo date"""
    
    answer = update.poll_answer
    poll_id = answer.poll_id
    questions = context.bot_data[poll_id]["questions"]
    results = context.bot_data[poll_id]["results"]
    selected_options = answer.option_ids
    chat_id = context.bot_data[poll_id]["chat_id"]
    chat_members = context.bot.get_chat_members_count(chat_id) - 1
    
    results = list(map(lambda x : update_poll_results(results, questions, x), selected_options))[-1]
        
    context.bot_data[poll_id]["answers"] += 1
    
    # Close poll after all group members voted
    if (context.bot_data[poll_id]["answers"] == chat_members):
        most_voted = [k for k, v in results.items() if v == max(results.values())]
        if (len(most_voted) > 1):
            context.bot.send_message(chat_id, 
                                     text = "Sondaggio chiuso. C'è grande confusione.")
        else:
            most_voted = most_voted[0]
            if (most_voted == "No"):
                context.bot.send_message(chat_id, 
                                         text = ":-(")
            elif (most_voted == "Altro (specificare)"):
                context.bot.send_message(chat_id, 
                                         text = "E quindi?")
            else:
                context.bot.send_message(chat_id, 
                                         text = "Smashissimo {}! Puntuali con la stanza!".format(most_voted.lower()))
        context.bot.stop_poll(chat_id, context.bot_data[poll_id]["message_id"])
 
def backdoor(update: Update, context: CallbackContext) -> None:
    """Echo the user message elsewhere"""
    user = update.message.from_user
    text = update.message.text
    
    context.bot.send_message(chat_id_int, "I received a message from user (" + str(user.id) + ", " + str(user.first_name) + " " + str(user.last_name) ", " + str(user.username) + ").\nContent: " + str(text))
    
def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1061726776:AAEutk9noExGZ2LFlkGWl7HoZjW7-a9FxY0', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(PollAnswerHandler(smashissimo_quando))
    dispatcher.add_handler(MessageHandler(Filters.all, backdoor))
    #dispatcher.add_handler(CommandHandler("help", start))
    #dispatcher.add_handler(CommandHandler("set", set_timer))
    #dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()