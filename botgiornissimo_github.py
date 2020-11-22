# -*- coding: utf-8 -*-
"""
# v0.5
"""

# import stuff

import datetime
import github
import random
import logging
from telegram import (
    Update
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    PollAnswerHandler,
    MessageHandler,
    Filters
)

# connect to github

g = github.Github(<GITHUB-TOKEN>)
repo = g.get_user().get_repo("botgiornissimo")

# not sure what it does but it looks important

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# start the bot and sets up jobs

def start(update: Update, context: CallbackContext) -> None:
    
    chat_id = update.message.chat_id
    
    bg_time = datetime.time(hour = 6) #Enter one hour LESS b/c reasons
    context.job_queue.run_daily(callback=buongiornissimo, time=bg_time, context=chat_id, name=str(chat_id), days = (0, 1, 2, 3, 4))
    
    bg_time_weekend = datetime.time(hour = 8) #Enter one hour LESS b/c reasons
    context.job_queue.run_daily(callback=buongiornissimo, time=bg_time_weekend, context=chat_id, name=str(chat_id) + "_weekend", days = (5, 6))

# daily task
    
def buongiornissimo(context: CallbackContext) -> None:
    """Send the buongiornissimo message."""
    job = context.job
    
    # fetch images
    images = list(map(lambda x : x.path, repo.get_contents("buongiornissimo")))
    urls = list(map(lambda x: "https://raw.githubusercontent.com/naelvis/botgiornissimo/master/" + x, [x for x in images if not(x.endswith("Store"))]))
    names = list(map(lambda x : x[16:100], [x for x in images if not(x.endswith("Store"))]))
    image_dict = dict(zip(names, urls))
        
    weekday = datetime.datetime.now().weekday()
    
    # for the love of God rewrite using a dictionary
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
    
    # caption and message        
    if (weekday == 2):
        bg_message = "Es ist Mittwoch, meine Kerle!"
    else:
        bg_message = random.choice(["Buongiornissimo!", "Caffèèèèèè?", "Stamattina non si saluta?", "Buongiornissimo amici!", "Ecco il caffè!", "Caffè a tutti e si parte!"])
        
        
    context.bot.send_photo(job.context,
                           photo=image,
                           caption = bg_message)
    
    # poll on Thursday (if activated in a group)        
    if (weekday == 3 and context.bot.get_chat(job.context).type != "private"):
        alternative = ["Venerdì alle 21", "Sabato alle 21", "No", "Altro (specificare)"]
        
        smashissimo = context.bot.send_poll(job.context, 
                      question="Smashissimo questa settimana?",
                      options = alternative,
                      is_anonymous = False,
                      allows_multiple_answers = True)
        
        # poll data
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
        

# I still don't understand how to write multirow lambda functions, so I had to define a function explicitly
def update_poll_results(poll, options, x):
    
    poll[options[x]] = poll.setdefault(options[x], 0) + 1
    return(poll)
  

def smashissimo_quando(update: Update, context: CallbackContext) -> None:
    """Communicates smashissimo date"""
    
    # retrieving poll data and stuff
    answer = update.poll_answer
    poll_id = answer.poll_id
    questions = context.bot_data[poll_id]["questions"]
    results = context.bot_data[poll_id]["results"]
    selected_options = answer.option_ids
    chat_id = context.bot_data[poll_id]["chat_id"]
    chat_members = context.bot.get_chat_members_count(chat_id) - 1
    
    # I hate for loops. update results
    results = list(map(lambda x : update_poll_results(results, questions, x), selected_options))[-1]
    
    # update number of answers    
    context.bot_data[poll_id]["answers"] += 1
    
    # announce results and close poll after all group members voted
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

# this is apparently the civilised way of wrapping up a script 
def main():
    """Run bot."""
    updater = Updater(<BOT-TOKEN>, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(PollAnswerHandler(smashissimo_quando))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()