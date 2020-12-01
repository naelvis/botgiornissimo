# -*- coding: utf-8 -*-
"""
# v1.0
"""

import logging
import modules
import telegram.ext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variables
REPLY = modules.remote.REPLY
CONTINUE = modules.augurissimi.CONTINUE

def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = telegram.ext.Updater(modules.tokens.tokenissimo, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # One-line handlers
    dispatcher.add_handler(telegram.ext.CommandHandler("start", modules.start.start))
    dispatcher.add_handler(telegram.ext.CommandHandler("stop", modules.start.stop))
    dispatcher.add_handler(telegram.ext.PollAnswerHandler(modules.start.smashissimo_quando))

    # Add conversation handler for remote start
    fallback_handler = [telegram.ext.MessageHandler(telegram.ext.Filters.all, modules.augurissimi.done)]
    remote_handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('remote', modules.remote.remote)],
        states={
            REPLY: [
                telegram.ext.MessageHandler(telegram.ext.Filters.all, modules.remote.remote_activation)
            ],
        },
        fallbacks=fallback_handler
    )
    dispatcher.add_handler(remote_handler)

    # Add conversation handler for events
    augurissimi_handler = [telegram.ext.MessageHandler(telegram.ext.Filters.all, modules.augurissimi.augurissimi)]
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