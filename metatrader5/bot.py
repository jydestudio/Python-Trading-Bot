import MetaTrader5 as mt5
import time

login = 5015914648
passcode = "wfcp3xwt"
server = "MetaQuotes-Demo"
symbol = "EURUSD"
lot = 0.01
time_frame = mt5.TIMEFRAME_M1
stop_loss = 15
take_profit = 30


def connect(account, password):
    if not mt5.initialize(login=account, password=password, server=server):
        print("Failed to connect to MetaTrader 5 terminal!")
        return False
    else:
        print("Connected successfully")
        login_result = mt5.login(account, password=password, server=server)

        if not login_result:
            print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
            print("Failed to log in to the MT5 account!", login_result)
            return False
        else:
            print(f"Logged in to MT5 account: {account}")

            return True


# Function to check if the candle is bullish
def is_bullish(candle):
    return candle[1] < candle[4]


def make_buy_order(symbol, lot, time_frame, stop_loss_price, take_profit_price):

    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "deviation": deviation,
        "magic": 234000,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": stop_loss_price,
        "tp": take_profit_price,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to open a buy order!")
        return False
    else:
        print(f"Buy order executed successfully at price: {mt5.symbol_info_tick(symbol).ask}")
        return True


def make_sell_order(symbol, lot, time_frame, stop_loss_price, take_profit_price):
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "deviation": deviation,
        "magic": 234000,
        "price": mt5.symbol_info_tick(symbol).bid,
        "sl": stop_loss_price,
        "tp": take_profit_price,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to open a sell order!")
        return False
    else:
        print(f"Sell order executed successfully at price: {mt5.symbol_info_tick(symbol).bid}")
        return True


def runBot(symbol, time_frame, lot, strategy, sl, tp):

    if strategy == "buy":
        number_of_buys = 0
        while True:
            candles = mt5.copy_rates_from_pos(symbol, time_frame, 0, 1)

            if True:
                symbol_info = mt5.symbol_info_tick(symbol)

                stop_loss_price = sl
                take_profit_price = tp
                # stop_loss_price = symbol_info.ask - stop_loss * mt5.symbol_info(symbol).point
                # take_profit_price = symbol_info.bid + take_profit * mt5.symbol_info(symbol).point

                for num in range(1, 51):
                    buy_status = make_buy_order(symbol, lot, time_frame, stop_loss_price, take_profit_price)

                    if buy_status:
                        number_of_buys += 1
                    else:
                        print("Last candle form wasn't a bullish candle skipping buy")

        time.sleep(60)

    elif strategy == "sell":
        number_of_sells = 0
        while True:
            candles = mt5.copy_rates_from_pos(symbol, time_frame, 0, 1)

            if not is_bullish(candles[0]):
                # Open a market order to sell
                symbol_info = mt5.symbol_info_tick(symbol)

                stop_loss = sl
                take_profit = tp
                stop_loss_price = symbol_info.bid + stop_loss * mt5.symbol_info(symbol).point
                take_profit_price = symbol_info.bid - take_profit * mt5.symbol_info(symbol).point

                sell_status = make_sell_order(symbol, lot, time_frame, stop_loss_price, take_profit_price)

                if sell_status:
                    number_of_sells += 1
            else:
                print("Last candle form wasn't a bearish candle skipping buy")
        time.sleep(60)


if connect(login, passcode):
    runBot(symbol, time_frame, lot, "buy", 1.09222, 1.09350)

else:
    print("Cannot connect to MetaTrader5 Terminal")
