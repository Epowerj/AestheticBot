
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging, os, urlparse2
from uuid import uuid4
from key import apikey #get the key from key.py

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Welcome to Aesrobot! Do /help for info')


def help(bot, update):
        bot.sendMessage(update.message.chat_id, text='Try using this bot inline!')


def vapor(text):
        return " ".join(text.upper())


def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Vapor",
                                            input_message_content=InputTextMessageContent(
                                                vapor(query)
                                            )))

    update.inline_query.answer(results)


def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
        TOKEN = apikey
        PORT = int(os.environ.get('PORT', '5000'))
        updater = Updater(TOKEN)
        dp = updater.dispatcher
        # add handlers
        updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
        updater.bot.setWebhook("https://" + str(os.environ.get("APPNAME")) + ".herokuapp.com/" + TOKEN)

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        dp.add_handler(InlineQueryHandler(inlinequery))

        #dp.add_handler(MessageHandler([Filters.text], echo))

        dp.add_error_handler(error)

        updater.idle()

if __name__ == '__main__':
        main()
