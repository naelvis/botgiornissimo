import datetime
import time
import telegram.ext
import telegram
import moduli.tokens as tokens
import subprocess
import os
import csv

ANALYSIS = 1

def smashammo(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    update.message.reply_text("E come è andata?")
    return ANALYSIS

def analysis(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:
    chat_id = update.message.chat_id

    update.message.document.get_file().download("{0}/results.jpg".format(tokens.pathissimo))
    update.message.reply_text("Ricevuto. Analisi in corso...")
    subprocess.call("/usr/local/bin/Rscript --vanilla {0}/ocr.r".format(tokens.pathissimo), shell=True)
    while not os.path.exists("{0}/results.csv".format(tokens.pathissimo)):
        time.sleep(1)
    with open("{0}/results.csv".format(tokens.pathissimo), newline='') as results:
        resultissimo = csv.reader(results, delimiter=',', quotechar='|')
        next(resultissimo)
        result_message = str()
        for row in resultissimo:
            result_message += str(': '.join(row))
            result_message += "\n"
        context.bot.send_message(chat_id, "Risultati registrati:\n{0}".format(result_message))
    with open("{0}/results.csv".format(tokens.pathissimo), newline='') as results:
        resultissimo = csv.reader(results, delimiter=',', quotechar='|')
        next(resultissimo)
        alessandro = next(resultissimo)[0]
        context.bot.send_message(chat_id, "Complimenti {0}!".format(alessandro))
    os.remove("{0}/results.csv".format(tokens.pathissimo))
    os.remove("{0}/results.csv".format(tokens.pathissimo))
    return telegram.ext.ConversationHandler.END

def e_allora(update: telegram.Update, context: telegram.ext.CallbackContext) -> int:

    update.message.reply_text("Sì, ma i risultati?")
    return ANALYSIS