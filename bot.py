import MetaTrader5 as mt5
import time


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
            price = mt5.symbol_info_tick(symbol).ask
            deviation = 20
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
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
                print(f"Buy order executed successfully at price: {symbol_info.ask}")

        # Sleep for 1 minute (60 seconds) before checking again

        for second in range(1, 61):
            print(f"{second} second(s)")
            time.sleep(1)

        print("Check candle again")


if __name__ == "__main__":
    main()
