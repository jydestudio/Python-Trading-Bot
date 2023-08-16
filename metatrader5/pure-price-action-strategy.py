import MetaTrader5 as mt5
import time
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)



# Function to check if the candle is bullish
def is_bullish(candle):
    return candle[1] < candle[4]


# Main function to connect, login, and execute buy orders on bullish candles (1-minute timeframe)
def main():

    # Replace these with your actual account credentials
    account = 5015914648
    password = "wfcp3xwt"
    server = "MetaQuotes-Demo"

    # Connect to the MT5 terminal
    if not mt5.initialize(login=account, password=password, server=server):
        print("Failed to connect to MetaTrader 5 terminal!")
        return

    # Replace this with the desired forex pair
    symbol = "EURUSD"

    # 1-minute timeframe
    time_frame = mt5.TIMEFRAME_M1

    # Attempt to log in to the account
    login_result = mt5.login(account, password=password, server=server)

    if not login_result:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
        print("Failed to log in to the MT5 account!", login_result)
        return

    print(f"Logged in to MT5 account: {account}")

    # Infinite loop for continuous monitoring
    while True:
        # Request the latest candle data
        candles = mt5.copy_rates_from_pos(symbol, time_frame, 0, 1)

        # Check if the current candle is bullish

        # print(candles)

        if is_bullish(candles[0]):
            # Open a market order to buy

            symbol_info = mt5.symbol_info_tick(symbol)

            lot = 0.1
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).bid
            deviation = 20
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": price,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
            }
            # send a trading request
            result = mt5.order_send(request)
            print(result)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Failed to open a buy order!")
            else:
                print(f"Sell order executed successfully at price: {symbol_info.bid}")

        # Sleep for 1 minute (60 seconds) before checking again

        else:
            print("Conditions not met, last candle not bearish.")

        print(f"Waiting for {time_frame}mins to execute next check.")
        time.sleep(60)

        print("Check candle again")


if __name__ == "__main__":
    main()




# import MetaTrader5 as mt5
# import time
# import numpy as np
#
# # Replace these with your actual account credentials
# account = 5015914648
# password = "wfcp3xwt"
# server = "MetaQuotes-Demo"
#
#
# # Connect to the MT5 terminal
# def connect_to_mt5():
#     if not mt5.initialize(login=account, password=password, server=server):
#         print("Failed to connect to MetaTrader 5 terminal!")
#         return
#
#     # Replace this with the desired forex pair
#     symbol = "EURUSD"
#
#     # 1-minute timeframe
#     time_frame = mt5.TIMEFRAME_M1
#
#     # Attempt to log in to the account
#     login_result = mt5.login(account, password=password, server=server)
#
#     if not login_result:
#         print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
#         print("Failed to log in to the MT5 account!", login_result)
#         return False
#
#     print(f"Logged in to MT5 account: {account}")
#     return True
#
#
# def check_price_action():
#     # Connect to the MT5 terminal
#     if not mt5.initialize():
#         print("Failed to connect to MetaTrader 5 terminal!")
#         return
#
#     # Replace these with your actual account credentials
#     # account = "your_mt5_account_number"
#     # password = "your_mt5_password"
#
#     # Replace this with the desired forex pair
#     symbol = "EURUSD"
#
#     # 1-minute timeframe
#     time_frame = mt5.TIMEFRAME_M1
#
#     # Check if the symbol is available
#     if not mt5.symbol_select(symbol):
#         print(f"Symbol {symbol} is not available!")
#         mt5.shutdown()
#         return
#
#     # Infinite loop for continuous monitoring
#     while True:
#         # Request the latest three candlesticks
#         candles = mt5.copy_rates_from_pos(symbol, time_frame, 0, 3)
#
#         # Check for bullish engulfing pattern
#         if is_bullish_engulfing(candles) and is_moving_average_crossover(candles):
#             print("Bullish Engulfing pattern detected.. Entering long position!")
#             ma_period = 20
#
#             # confirming signal before placing a buy order
#             wait_for_confirmation(symbol, ma_period)
#
#             enter_long_position(symbol)
#
#         elif is_hammer(candles):
#             print("Hammer pattern detect... Entering long position")
#             enter_long_position(symbol)
#
#         # elif is_inverted_hammer(candles):
#         #     print("Inverted Hammer pattern detect... Entering long position")
#         #     enter_long_position(symbol)
#
#         elif is_three_white_soldiers(candles):
#             print("Three white soldiers pattern detect... Entering long position")
#             enter_long_position(symbol)
#
#         elif is_bullish_harami(candles):
#             print("Bullish Harami patterm detect... Entering long position")
#             enter_long_position(symbol)
#
#         else:
#             print("conditions not met cannot buy at this time... waiting for another 1 minutes....")
#
#         # Sleep for 1 minute before checking again
#         time.sleep(60)
#
#
# def follow_trend():
#     symbol = "EURUSD"
#     timeframe = mt5.TIMEFRAME_M1
#
#     while True:
#         rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 2)
#         current_close = rates[0][4]
#         previous_close = rates[1][4]
#
#         # Calculate Moving Averages
#         fast_ma = sum([rate[4] for rate in rates[-10:]]) / 10
#         slow_ma = sum([rate[4] for rate in rates[-50:]]) / 50
#
#         if current_close > fast_ma and current_close > slow_ma >= previous_close:
#             # If conditions are met, execute a Buy trade
#             print("Executing Buy trade")
#             enter_long_position(symbol)
#             # Code to execute a Buy trade
#
#         elif current_close < fast_ma and current_close < slow_ma <= previous_close:
#             # If conditions are met, execute a Sell trade
#             print("Executing Sell trade")
#             enter_short_position(symbol)
#             # Code to execute a Sell trade
#
#         else:
#             print("No trend found. Skipping buy")
#
#         time.sleep(60)  # Wait for 1 minute before checking again
#
#
# def moving_average(data, period):
#     weights = np.ones(period) / period
#     return np.convolve(data, weights, mode='valid')
#
#
# def wait_for_confirmation(symbol, ma_period):
#     # Wait for the moving average crossover
#     while True:
#         # Get historical candlestick data
#         rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, ma_period)
#
#         if rates is None or len(rates) < ma_period:
#             print("Insufficient historical data to calculate moving average.")
#             break
#
#         # Extract the data from the historical rates
#         close_prices = [rate['close'] for rate in rates]
#
#         # Calculate the moving average
#         ma = moving_average(close_prices, ma_period)
#
#         current_price = mt5.symbol_info_tick(symbol).ask
#
#         if current_price > ma[-1]:
#             break
#
#
# def is_bullish_engulfing(candles):
#     open_prices = [candle['open'] for candle in candles]
#     close_prices = [candle['close'] for candle in candles]
#
#     # Check for bullish engulfing pattern
#     if open_prices[1] > close_prices[1] and close_prices[1] < open_prices[0] < close_prices[0]:
#         return True
#
#     return False
#
#
# def is_moving_average_crossover(candles):
#     # Calculate 20-period and 50-period moving averages
#     ma20 = sum(c['close'] for c in candles[:-1]) / len(candles[:-1])
#     ma50 = sum(c['close'] for c in candles[:-2]) / len(candles[:-2])
#
#     # Check for moving average crossover
#     if ma50 < ma20 < candles[-1]['close']:
#         return True
#     return False
#
#
# def is_hammer(candles):
#     if len(candles) < 1:
#         return False
#
#     current_open = candles[-1]['open']
#     current_close = candles[-1]['close']
#     current_high = candles[-1]['high']
#     current_low = candles[-1]['low']
#
#     # Check for a hammer pattern
#     if current_high - current_low > 2 * (current_open - current_close) and \
#        current_close > current_open and \
#        (current_close - current_low) / (current_high - current_low) >= 0.6:
#         return True
#
#     return False
#
#
# def is_inverted_hammer(candles):
#     if len(candles) < 1:
#         return False
#
#     current_open = candles[-1]['open']
#     current_close = candles[-1]['close']
#     current_high = candles[-1]['high']
#     current_low = candles[-1]['low']
#
#     # Check for an inverted hammer pattern
#     if current_high - current_low > 2 * (current_close - current_open) and \
#        current_close < current_open and \
#        (current_high - current_close) / (current_high - current_low) >= 0.6:
#         return True
#
#     return False
#
#
# def is_three_white_soldiers(candles):
#     if len(candles) < 3:
#         return False
#
#     # Check for three consecutive bullish candles
#     if candles[-3]['close'] > candles[-3]['open'] and \
#             candles[-2]['close'] > candles[-2]['open'] and \
#             candles[-1]['close'] > candles[-1]['open']:
#
#         # Check if each candle opens higher than the previous one
#         if candles[-3]['open'] < candles[-2]['open'] < candles[-1]['open']:
#
#             # Check if each candle closes near its high
#             if candles[-3]['close'] >= candles[-3]['close'] - 0.2 * (candles[-3]['close'] - candles[-3]['open']) and \
#                     candles[-2]['close'] >= candles[-2]['close'] - 0.2 * (
#                     candles[-2]['close'] - candles[-2]['open']) and \
#                     candles[-1]['close'] >= candles[-1]['close'] - 0.2 * (candles[-1]['close'] - candles[-1]['open']):
#                 return True
#
#     return False
#
#
# def is_bullish_harami(candles):
#     if len(candles) < 2:
#         return False
#
#     # Check for two consecutive candles
#     first_candle = candles[-2]
#     second_candle = candles[-1]
#
#     # Check if the first candle is bearish and the second candle is bullish
#     if first_candle['close'] < first_candle['open'] and \
#        second_candle['close'] > second_candle['open']:
#
#         # Check if the second candle's body is completely contained within the first candle's body
#         if first_candle['open'] > second_candle['close'] and \
#            first_candle['close'] < second_candle['open']:
#             return True
#
#     return False
#
#
# def enter_long_position(symbol):
#     # Replace this with your desired position size and risk percentage
#     print("Starting entry to long position")
#
#     stop_loss = 15  # pips
#     take_profit = 5  # pips
#
#     # Place a buy order at the current market price
#     current_price = mt5.symbol_info_tick(symbol).ask
#
#     lot = 0.1  # Calculate lot size based on risk
#
#     # Request the current market price
#     symbol_info = mt5.symbol_info_tick(symbol)
#     if symbol_info is None:
#         print(f"Failed to get tick data for {symbol}!")
#         return
#
#     # Calculate the stop loss and take profit levels
#     stop_loss_price = symbol_info.ask - stop_loss * mt5.symbol_info(symbol).point
#     take_profit_price = symbol_info.ask + take_profit * mt5.symbol_info(symbol).point
#     deviation = 20
#
#     # Open a market order to buy
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY,
#         "deviation": deviation,
#         "magic": 234000,
#         "price": mt5.symbol_info_tick(symbol).ask,
#         "sl": stop_loss_price,
#         "tp": take_profit_price,
#         "comment": "python script open",
#         "type_time": mt5.ORDER_TIME_GTC,
#     }
#
#     # send a trading request
#     result = mt5.order_send(request)
#
#     if result.retcode != mt5.TRADE_RETCODE_DONE:
#         print("2. order_send failed, retcode={}".format(result.retcode))
#         print("Failed to open a buy order!")
#     else:
#         print(f"Buy order executed successfully at price: {symbol_info.ask}")
#
#
# def enter_short_position(symbol):
#     # Replace this with your desired position size and risk percentage
#     print("Starting entry to long position")
#
#     stop_loss = 15  # pips
#     take_profit = 5  # pips
#
#     # Place a buy order at the current market price
#     current_price = mt5.symbol_info_tick(symbol).ask
#
#     lot = 0.1  # Calculate lot size based on risk
#
#     # Request the current market price
#     symbol_info = mt5.symbol_info_tick(symbol)
#     if symbol_info is None:
#         print(f"Failed to get tick data for {symbol}!")
#         return
#
#     # Calculate the stop loss and take profit levels
#     stop_loss_price = symbol_info.bid + stop_loss * mt5.symbol_info(symbol).point
#     take_profit_price = symbol_info.bid - take_profit * mt5.symbol_info(symbol).point
#     deviation = 20
#
#     # Open a market order to buy
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY,
#         "deviation": deviation,
#         "magic": 234000,
#         "price": mt5.symbol_info_tick(symbol).bid,
#         "sl": stop_loss_price,
#         "tp": take_profit_price,
#         "comment": "python script open",
#         "type_time": mt5.ORDER_TIME_GTC,
#     }
#
#     # send a trading request
#     result = mt5.order_send(request)
#
#     if result.retcode != mt5.TRADE_RETCODE_DONE:
#         print("2. order_send failed, retcode={}".format(result.retcode))
#         print("Failed to open a sell order!")
#     else:
#         print(f"Sell order executed successfully at price: {symbol_info.bid}")
#
#
# if __name__ == "__main__":
#     if connect_to_mt5():
#         follow_trend()
#
#
#
#
# # Name: akinjide lawrence
# # Server: MetaQuotes-Demo
# # Type: Forex Hedged USD
# # Login: 72346574
# # Password: 0gnzzeus
# # Investor: qyb3vovc