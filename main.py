# -*- coding: utf-8 -*-
"""
# v1.0
"""

import logging
import moduli.remote as remote
import moduli.augurissimi as augurissimi
import moduli.tokens as tokens
import moduli.start as start
import moduli.smashissimo as smashissimo
import moduli.ocrissimo as ocrissimo
import telegram.ext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variables
REPLY = remote.REPLY
CONTINUE = augurissimi.CONTINUE
ANALYSIS = ocrissimo.ANALYSIS

def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = telegram.ext.Updater(tokens.tokenissimo, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # One-line handlers
    dispatcher.add_handler(telegram.ext.CommandHandler("start", start.start))
    dispatcher.add_handler(telegram.ext.CommandHandler("stop", start.stop))
    dispatcher.add_handler(telegram.ext.PollAnswerHandler(smashissimo.smashissimo_quando))

    # Add conversation handler for registering match result
    remote_handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('smashammo', ocrissimo.smashammo)],
        states={
            ANALYSIS: [
                telegram.ext.MessageHandler(telegram.ext.Filters.document, ocrissimo.analysis)
            ],
        },
        fallbacks= [telegram.ext.MessageHandler(telegram.ext.Filters.all, ocrissimo.e_allora)]
    )
    dispatcher.add_handler(remote_handler)

    # Add conversation handler for remote start
    fallback_handler = [telegram.ext.MessageHandler(telegram.ext.Filters.all, augurissimi.done)]
    remote_handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('remote', remote.remote)],
        states={
            REPLY: [
                telegram.ext.MessageHandler(telegram.ext.Filters.all, remote.remote_activation)
            ],
        },
        fallbacks=fallback_handler
    )
    dispatcher.add_handler(remote_handler)

    # Add conversation handler for events
    augurissimi_handler = [telegram.ext.MessageHandler(telegram.ext.Filters.all, augurissimi.augurissimi)]
    event_handler = telegram.ext.ConversationHandler(
        entry_points=augurissimi_handler,
        states={
            CONTINUE: augurissimi_handler
        },
        fallbacks=fallback_handler
    )
    dispatcher.add_handler(event_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()