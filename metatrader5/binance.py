import time
from binance import Client


# Function to check if the candle is bullish
def is_bullish(candle):
    return candle[1] < candle[4]


# Main function to connect, login, and execute buy orders on bullish candles (1-minute timeframe)
def main():
    # Replace these with your actual API key and secret
    api_key = "t0rqeDZiynUCgKkDul7M3w8D2uNOxMpj6ojxNcg9CvEHewTqa85Rzh1kmmbZ9ucK"
    api_secret = "RPJOV6Owrm0qPFDiu6QTY3cWc661KKGJUGRyFawW4Clb9CuIKKwQ0A2i9On4VeaN"

    client = Client(api_key=api_key, api_secret=api_secret, testnet=True)

    # Replace this with the desired trading pair
    symbol = 'SOLUSDT'

    # Infinite loop for continuous monitoring
    while True:
        # Request the latest candle data
        candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)

        # Check if the current candle is bullish
        if is_bullish(candles[0]):
            # Open a market order to sell
            lot = 0.1
            price = float(candles[0][4])  # Closing price of the current candle
            try:
                order = client.create_test_order(
                    symbol=symbol,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=lot
                )
                print(order)
                print("Sell order executed successfully at price:", price)
            except Exception as e:
                print("Failed to open a sell order:", e)
        else:
            print("Conditions not met, last candle not bullish.")

        print("Waiting for 1 minute to execute next check.")
        time.sleep(60)


if __name__ == "__main__":
    main()
