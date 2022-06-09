import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from tracker import get_prices, get_coins, get_price
import config

updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
    message = f"Welcome to Bot Midas! Here are the commands.\n/start - " \
              f"Start the telegram bot\n/current_prices - Show " \
              f"all current prices for most of the cryptocurencies\n/show_coins - Shows all the currencies "

    context.bot.send_message(chat_id=chat_id, text=message)


def show_coins(update, context):
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_coins()
    for i in crypto_data:
        coin = i
        message += f"{coin}\n"
    context.bot.send_message(chat_id, text=message)


def show_prices(update, context):
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)

def show_price(update, context):
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_price()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("current_prices", show_prices))
dispatcher.add_handler(CommandHandler("show_coins", show_coins))
dispatcher.add_handler(CommandHandler("show_price", show_price))
updater.start_polling()
