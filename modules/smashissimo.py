import datetime
import random
import github
import telegram.ext
import telegram
import modules.augurissimi as augurissimi

import modules.tokens as tokens

payload = dict()

def buongiornissimo(context: telegram.ext.CallbackContext) -> None:
    """Send the pictures message."""
    job = context.job

    # get images
    images = list(map(lambda x: x.path, github.Github(tokens.githubissimo).get_user().get_repo("pictures").get_contents("pictures")))
    urls = list(map(lambda x: "https://raw.githubusercontent.com/naelvis/botgiornissimo/master/" + x,
                    [x for x in images if not (x.endswith("Store"))]))
    names = list(map(lambda x: x[16:100], [x for x in images if not (x.endswith("Store"))]))
    image_dict = dict(zip(names, urls))

    weekday = datetime.datetime.now().weekday()
    [day, month] = [datetime.datetime.now().day, datetime.datetime.now().month]

    # this looks as if it was written by a monkey
    if (weekday == 0):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("LU") | key.startswith("X"))}
    elif (weekday == 1):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("MA") | key.startswith("X"))}
    elif (weekday == 2):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("Mitt"))}
    elif (weekday == 3):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("GI") | key.startswith("X"))}
    elif (weekday == 4):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("VE") | key.startswith("X"))}
    elif (weekday == 5):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("SA") | key.startswith("X"))}
    elif (weekday == 6):
        dict_subset = {key: value for key, value in image_dict.items() if (key.startswith("DO") | key.startswith("X"))}

    image = random.choice(list(dict_subset.values()))

    if (job.context != tokens.gruppissimo or not ([day, month] in augurissimi.Events_daymonth.values())):
        if (weekday == 2):
            bg_message = "Es ist Mittwoch, meine Kerle!"
        else:
            bg_message = random.choice(
                ["Buongiornissimo!", "Caffèèèèèè?", "Stamattina non si saluta?", "Buongiornissimo amici!",
                 "Ecco il caffè!", "Caffè per tutti e si parte!"])

    context.bot.send_photo(job.context,
                           photo=image,
                           caption=bg_message)

    if (weekday == 3 and job.context == tokens.gruppissimo):
        alternative = ["Venerdì alle 21", "Sabato alle 21", "No", "Altro (specificare)"]

        smashissimo = context.bot.send_poll(job.context,
                                            question="Smashissimo questa settimana?",
                                            options=alternative,
                                            is_anonymous=False,
                                            allows_multiple_answers=True)

        payload[smashissimo.poll.id] = payload.setdefault(smashissimo.poll.id,
                                                          {
                                                              "questions": alternative,
                                                              "message_id": smashissimo.message_id,
                                                              "chat_id": job.context,
                                                              "answers": 0,
                                                              "results": dict()
                                                          })

        context.bot_data.update(payload)

def update_poll_results(poll, options, x):
    poll[options[x]] = poll.setdefault(options[x], 0) + 1
    return (poll)

def smashissimo_quando(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    """Communicates smashissimo date"""

    answer = update.poll_answer
    poll_id = answer.poll_id
    questions = context.bot_data[poll_id]["questions"]
    results = context.bot_data[poll_id]["results"]
    selected_options = answer.option_ids
    chat_id = context.bot_data[poll_id]["chat_id"]
    chat_members = context.bot.get_chat_members_count(chat_id) - 1

    # I hate for loops
    results = list(map(lambda x: update_poll_results(results, questions, x), selected_options))[-1]

    context.bot_data[poll_id]["answers"] += 1

    # Close poll after all group members voted
    if (context.bot_data[poll_id]["answers"] == chat_members):
        most_voted = [k for k, v in results.items() if v == max(results.values())]
        if (len(most_voted) > 1):
            context.bot.send_message(chat_id,
                                     text="Sondaggio chiuso. C'è grande confusione.")
        else:
            most_voted = most_voted[0]
            if (most_voted == "No"):
                context.bot.send_message(chat_id,
                                         text=":-(")
            elif (most_voted == "Altro (specificare)"):
                context.bot.send_message(chat_id,
                                         text="E quindi?")
            else:
                context.bot.send_message(chat_id,
                                         text="Smashissimo {}! Puntuali con la stanza!".format(most_voted.lower()))
        context.bot.stop_poll(chat_id, context.bot_data[poll_id]["message_id"])