import pandas as pd
import time
import requests
import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
from tracker import get_prices, get_price, get_coins
import config

updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
loop_state = True


def start(update, context):
    chat_id = update.effective_chat.id
    message = f"Welcome to Bot Midas! Here are the commands.\n/start - " \
              f"Start the telegram bot\n/current_prices - Show " \
              f"all current prices for most of the cryptocurencies\n/show_coins - Shows all the currencies\n/show_price - Shows price of a BTC(Bitcoin)\n" \
              f"/start_signals - Starts the loop of the signals based on RSI\n/decision - Bot gives you advice about " \
              f"next actions "

    context.bot.send_message(chat_id=chat_id, text=message)



def start_signals(update, context):
    chat_id = update.effective_chat.id
    while loop_state:
        coin = 'BTCUSDT'
        time_interval = 5

        link = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + coin + '&interval=' + str(
            time_interval) + 'm' + '&limit=100'
        data = requests.get(link).json()

        data_frame = pd.DataFrame(data)
        data_frame.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades',
                     'taker_base_vol', 'taker_quote_vol', 'is_best_match']

        period = 14
        d = data_frame
        d['close'] = d['close'].astype(float)
        d2 = d['close'].to_numpy()

        d2 = pd.DataFrame(d2, columns=['close'])
        delta = d2.diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        profit = up.ewm(com=(period - 1), min_periods=period).mean()
        loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = profit / loss

        rsi = 100 - (100 / (1 + RS))
        rsi = rsi['close'].iloc[-1]
        rsi = round(rsi, 1)

        text = 'Trading state Bitcoin (BTC) RSI: ' + str(rsi)

        print(text)
        bot.send_message(chat_id=chat_id, text=text)

        time.sleep(5)



def decision(update, context):
    coin = 'BTCUSDT'
    time_interval = 5

    link = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + coin + '&interval=' + str(
        time_interval) + 'm' + '&limit=100'
    data = requests.get(link).json()

    data_frame = pd.DataFrame(data)
    data_frame.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'is_best_match']

    period = 14
    d = data_frame
    d['close'] = d['close'].astype(float)
    d2 = d['close'].to_numpy()

    d2 = pd.DataFrame(d2, columns=['close'])
    delta = d2.diff()

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    profit = up.ewm(com=(period - 1), min_periods=period).mean()
    loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = profit / loss
    rsi = 100 - (100 / (1 + RS))
    rsi = rsi['close'].iloc[-1]
    rsi = round(rsi, 1)

    if rsi <= 30:
        text = 'RSI is ' + str(rsi) + '. So, advice is to BUY.'
    elif 30 < rsi < 70:
        text = 'RSI is ' + str(rsi) + '. So, advice is to KEEP.'
    else:
        text = 'RSI is ' + str(rsi) + '. So, advice is to SELL.'

    chat_id = update.effective_chat.id

    context.bot.send_message(chat_id=chat_id, text=text)


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
dispatcher.add_handler(CommandHandler("decision", decision))
dispatcher.add_handler(CommandHandler("start_signals", start_signals))
updater.start_polling()