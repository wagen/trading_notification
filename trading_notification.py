from typing import Counter
import websocket
import threading
import time
import json
import statistics
import telegram

def on_message(ws, message):
    #print(message)
    data_stream = json.loads(message)
    if("data" in data_stream):
        symbol = data_stream["data"]["s"]
        open_price = float(data_stream["data"]["k"]["o"])
        close_price = float(data_stream["data"]["k"]["c"])
        price_change = (close_price - open_price)/open_price
        closed = data_stream["data"]["k"]["x"]
        volume = float(data_stream["data"]["k"]["v"])
        if(closed):         
            store_volume_history(symbol, volume)
            if(price_change >= 0.01):
                #if(store_volume_history(volume) != 0 and store_volume_history(volume) < volume):
                if(len(hourly_volume[symbol]) == 60 and statistics.median(hourly_volume[symbol]) < volume):
                    order = "Buy " +  symbol + ": {}."
                    print(order.format(close_price))
                    print("Volume: " + data_stream["data"]["k"]["v"])
                    print(time.ctime(data_stream["data"]["k"]["T"] / 1000))
                    send_telegram_message(order.format(close_price))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params":
        [
        "adausdt@kline_1m",
        "bnbusdt@kline_1m",
        "btcusdt@kline_1m",
        "bttusdt@kline_1m",
        "dashusdt@kline_1m",
        "dogeusdt@kline_1m",
        "dotusdt@kline_1m",
        "ethusdt@kline_1m",
        "filusdt@kline_1m",
        "icpusdt@kline_1m",
        "linkusdt@kline_1m",
        "runeusdt@kline_1m",
        "solusdt@kline_1m",
        "uniusdt@kline_1m",
        "xmrusdt@kline_1m",
        "xrpusdt@kline_1m",
        ],
        "id": 1
    }))
    
    def run(*args):
        #ws.close()
        print("Monitoring...")

    threading.Thread(target = run).start()

hourly_volume = {}
def store_volume_history(symbol, volume):
    global hourly_volume

    if(symbol in hourly_volume.keys()):
        if(len(hourly_volume[symbol]) == 60):
            hourly_volume[symbol].pop(0)
            hourly_volume[symbol].append(volume)
            """f = open("volume_log.txt", "w")
            f.write(json.dumps(hourly_volume))
            f.close()"""
        else:
            hourly_volume[symbol].append(volume)
    else:
        hourly_volume[symbol] = [volume]
            

    

def send_telegram_message(message):
    bot = telegram.Bot(token = "---your token---")
    bot.send_message(chat_id = ---chatid---, text=message)
    bot.send_message(chat_id = ---cahtid---, text=message)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/stream?streams=",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    

    ws.run_forever()