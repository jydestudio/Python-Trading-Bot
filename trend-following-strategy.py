import MetaTrader5 as mt5

# Replace with your desired risk percentage per trade (e.g., 2%)
risk_percentage = 2

# Replace these with your actual account credentials
account = 5015914648
password = "wfcp3xwt"
server = "MetaQuotes-Demo"


# Connect to the MT5 terminal
def connect_to_mt5():
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
        return False

    print(f"Logged in to MT5 account: {account}")
    return True


def get_account_balance():
    account_info = mt5.account_info()
    return account_info.balance


def calculate_position_size(balance, risk_percentage, stop_loss):
    # Calculate position size based on risk percentage and stop loss
    position_size = (balance * risk_percentage) / (stop_loss / 100)
    return position_size


def moving_average_crossover_strategy(symbol, short_period, long_period):
    # Get the current account balance
    account_balance = get_account_balance()

    # Get the current tick data for the symbol
    tick = mt5.symbol_info_tick(symbol)

    # Calculate stop loss and take profit levels
    stop_loss = 100  # Replace with your desired stop loss value (e.g., 100 pips for Forex)
    take_profit = 200  # Replace with your desired take profit value (e.g., 200 pips for Forex)

    # Calculate position size based on risk management
    position_size = calculate_position_size(account_balance, risk_percentage, stop_loss)

    # Get historical data for the moving averages
    short_ma_data = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 1, short_period)
    long_ma_data = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 1, long_period)

    # Calculate the moving averages
    short_ma = sum(bar['close'] for bar in short_ma_data) / short_period
    long_ma = sum(bar['close'] for bar in long_ma_data) / long_period

    # Check for crossover signals
    if short_ma > long_ma:
        # Go long (buy)
        print("Signal: Go Long (Buy)")
        print("Price:", tick.ask)
        print("Stop Loss:", tick.ask - stop_loss)
        print("Take Profit:", tick.ask + take_profit)
        print("Position Size:", position_size)
        # Implement code to place a buy order here (using mt5.order_send())

        volume = 0.1
        stop_loss = 50  # pips
        take_profit = 100  # pips

        # Request the current market price
        symbol_info = mt5.symbol_info_tick(symbol)
        if symbol_info is None:
            print(f"Failed to get tick data for {symbol}!")
            return

        # Calculate the stop loss and take profit levels
        stop_loss_price = symbol_info.ask - stop_loss * mt5.symbol_info(symbol).point
        take_profit_price = symbol_info.ask + take_profit * mt5.symbol_info(symbol).point
        deviation = 20
        lot = 0.1

        # Open a market order to buy
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

        # send a trading request
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            print("Failed to open a buy order!")
        else:
            print(f"Buy order executed successfully at price: {symbol_info.ask}")

    elif short_ma < long_ma:
        # Go short (sell)
        print("Signal: Go Short (Sell)")
        print("Price:", tick.bid)
        print("Stop Loss:", tick.bid + stop_loss)
        print("Take Profit:", tick.bid - take_profit)
        print("Position Size:", position_size)
        # Implement code to place a sell order here (using mt5.order_send())

        volume = 0.1
        stop_loss = 50  # pips
        take_profit = 100  # pips

        # Request the current market price
        symbol_info = mt5.symbol_info_tick(symbol)
        if symbol_info is None:
            print(f"Failed to get tick data for {symbol}!")
            return

        # Calculate the stop loss and take profit levels
        stop_loss_price = symbol_info.ask + stop_loss * mt5.symbol_info(symbol).point
        take_profit_price = symbol_info.ask - take_profit * mt5.symbol_info(symbol).point
        deviation = 20
        lot = 0.1

        # Open a market order to buy
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "deviation": deviation,
            "magic": 234000,
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": stop_loss_price,
            "tp": take_profit_price,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
        }
        # send a trading request
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            print("Failed to open a sell order!")
        else:
            print(f"Sell order executed successfully at price: {symbol_info.ask}")

def main():
    connect_to_mt5()

    # Replace with the symbol of the instrument you want to trade (e.g., "EURUSD")
    symbol = "EURUSD"
    short_period = 50  # Replace with your desired short-term moving average period
    long_period = 200  # Replace with your desired long-term moving average period

    moving_average_crossover_strategy(symbol, short_period, long_period)

    mt5.shutdown()


if __name__ == "__main__":
    connect_to_mt5()

    volume = 0.1
    stop_loss = 50  # pips
    take_profit = 100  # pips

    # Request the current market price
    symbol = "EURUSD"
    symbol_info = mt5.symbol_info_tick(symbol)

    if symbol_info is None:
        print(f"Failed to get tick data for EURUSD!")
        pass

    # Calculate the stop loss and take profit levels
    stop_loss_price = symbol_info.ask - stop_loss * mt5.symbol_info("EURUSD").point
    take_profit_price = symbol_info.ask + take_profit * mt5.symbol_info("EURUSD").point
    deviation = 20
    lot = 0.1
    symbol = "EURUSD"

    # Open a market order to buy
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

    # send a trading request
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        print("Failed to open a buy order!")
    else:
        print(f"Buy order executed successfully at price: {symbol_info.ask}")


    main()
