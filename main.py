# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Indicators
import Other
import json
from datetime import datetime, timedelta
import pynput
from pynput.mouse import Button, Controller
# from pynput.keyboard import Key, Controller

mouse = Controller()
# keyboard = Controller()


def init():
    Indicators.dumpcur("GBP_USD")
    Indicators.dumphis("GBP_USD", "M30")
    Indicators.machis()
    Indicators.atrhis()
    Indicators.cmfhis()


def back():
    con3 = False
    init()
    with open("5M.json", "r") as read:
        data = json.load(read)
    with open("cur.json", "r") as read:
        cur = json.load(read)
    # buys are bid
    # sells are asks
    bid = float(cur["prices"][0]["bids"][0]["price"])
    asks = float(cur["prices"][0]["asks"][0]["price"])
    for i in range(46, len(data)):
        if float(data[i]["macd"][0]) > 0.0003 and float(data[i]["macd"][1]) > 0.0003:
            con1 = float(data[i-1]["macd"][0]) < float(data[i-1]["macd"][1])
            con2 = float(data[i]["macd"][0]) > float(data[i]["macd"][1])
            if float(data[i]["cmf"]) > 0:
                con3 = True
            elif float(data[i]["cmf"]) == 0 and float(data[i-1]["cmf"]) > 0:
                con3 = True
            else:
                con3 = False
            if con1 and con2 and con3:
                sl = bid - float(data[i]["atr"]) * 2
                tp = bid + float(data[i]["atr"]) * 4
                print("buy", data[i]["time"], data[i]["atr"])
            elif float(data[i-1]["macd"][0]) < 0 or float(data[i-1]["macd"][1]) < 0:
                # place the order, possibly create a new function to do this
                print("buy", data[i]["time"], data[i]["atr"])
        elif float(data[i]["macd"][0]) < 0.0003 and float(data[i]["macd"][1]) < 0.0003:
            con1 = float(data[i-1]["macd"][0]) > float(data[i-1]["macd"][1])
            con2 = float(data[i]["macd"][0]) < float(data[i]["macd"][1])
            if float(data[i]["cmf"]) < 0:
                con3 = True
            elif float(data[i]["cmf"]) == 0 and float(data[i-1]["cmf"]) < 0:
                con3 = True
            else:
                con3 = False
            if con1 and con2 and con3:
                print("sell", data[i]["time"], data[i]["atr"])
            elif float(data[i-1]["macd"][0]) > 0 or float(data[i-1]["macd"][1]) > 0:
                # place the order, possibly create a new function to do this
                print("sell", data[i]["time"], data[i]["atr"])


def live(pair):
    con3 = False
    proper = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("5M.json", "r") as read:
        data = json.load(read)
    with open("cur.json", "r") as read:
        cur = json.load(read)
    with open("Orders.json", "r") as read:
        orders = json.load(read)
    # buys are bid
    # sells are asks
    bid = float(cur["prices"][0]["bids"][0]["price"])
    asks = float(cur["prices"][0]["asks"][0]["price"])

    init()
    # Indicators.dumpcur(pair)
    # Indicators.dumphis(pair, "M30")
    # Indicators.machis()
    # Indicators.atrhis()
    # Indicators.cmfhis()
    if float(data[-2]["macd"][0]) > 0 and float(data[-2]["macd"][1]) > 0:
        con1 = float(data[-3]["macd"][0]) < float(data[-3]["macd"][1])
        con2 = float(data[-2]["macd"][0]) > float(data[-2]["macd"][1])
        if float(data[-2]["cmf"]) > 0:
            con3 = True
        elif float(data[-2]["cmf"]) == 0 and float(data[-2]["cmf"]) > 0:
            con3 = True
        else:
            con3 = False
        if con1 and con2 and con3 and (float(data[-2]["macd"][0]) > 0.0003 or float(data[-2]["macd"][1]) > 0.0003):
            # place the order, possibly create a new function to do this
            tp = bid + (float(data[-2]["atr"]) * 4)
            sl = bid - (float(data[-2]["atr"]) * 2)
            place(pair, tp, sl, bid, proper)
        elif float(data[-3]["macd"][0]) < 0 or float(data[-3]["macd"][1]) < 0:
            # place the order, possibly create a new function to do this
            tp = bid + (float(data[-2]["atr"]) * 4)
            sl = bid - (float(data[-2]["atr"]) * 2)
            place(pair, tp, sl, bid, proper)
    elif float(data[-2]["macd"][0]) < 0 and float(data[-2]["macd"][1]) < 0:
        con1 = float(data[-3]["macd"][0]) > float(data[-3]["macd"][1])
        con2 = float(data[-2]["macd"][0]) < float(data[-2]["macd"][1])
        if float(data[-2]["cmf"]) < 0:
            con3 = True
        elif float(data[-2]["cmf"]) == 0 and float(data[-2]["cmf"]) < 0:
            con3 = True
        else:
            con3 = False
        if con1 and con2 and con3 and (float(data[-2]["macd"][0]) < 0.0003 or float(data[-2]["macd"][1]) < 0.0003):
            tp = asks - (float(data[-2]["atr"]) * 4)
            sl = asks + (float(data[-2]["atr"]) * 2)
            # place the order, possibly create a new function to do this
            place(pair, tp, sl, asks, proper)
        elif float(data[-3]["macd"][0]) > 0 or float(data[-3]["macd"][1]) > 0:
            # place the order, possibly create a new function to do this
            tp = asks - (float(data[-2]["atr"]) * 4)
            sl = asks + (float(data[-2]["atr"]) * 2)
            place(pair, tp, sl, asks, proper)
    # else:
    #     watch(pair)


def place(pair, tp, sl, cur, time, lot="0.01"):
    with open("Orders.json", "r") as read:
        order = json.load(read)
    pair_list = {
        "GBP_CAD": []
    }
    if float(tp) > float(cur):
        order[pair]["open"].append(["buy", cur, sl, tp, time, lot])
    elif float(tp) < float(cur):
        order[pair]["open"].append(["sell", cur, sl, tp, time, lot])
    with open("Orders.json", "w") as out:
        out.write(json.dumps(order, indent=4))
    # mouse.position = pair_list[pair]
    # mouse.click(Button.left, 2)
    # keyboard.type("123")


def modify(change):
    if change == "be":
        mouse.position = [123, 123]


def watch(pair):
    Indicators.dumpcur(pair)
    now = datetime.now()
    with open("Orders.json", "r") as read:
        orders = json.load(read)
    with open("cur.json", "r") as read:
        cur = json.load(read)
    bid = float(cur["prices"][0]["bids"][0]["price"])
    asks = float(cur["prices"][0]["asks"][0]["price"])
    for i in orders[pair]["open"]:
        start = float(i[1])
        if i[0] == "buy":
            if bid > start + Other.converter("price", 10, pair):
                modify("be")
        elif i[0] == "sell":
            if asks < start - Other.converter("price", 10, pair):
                modify("be")


Indicators.dumphis("GBP_USD", "M5", "5M.json")
Indicators.dumphis("GBP_USD", "M15", "15M.json")
Indicators.dumphis("GBP_USD", "M15", "1H.json")
Indicators.machis()
Indicators.emaTime("15M.json")
Indicators.emaTime("1H.json")

# result = Indicators.supres()
#
# print(result[0])
#
# print(result[1])

# with open("5M.json", "r") as read:
#     data = json.load(read)
# print(float(data[0]["mid"]["h"]))

# watch("GBP_CAD")
# back()
# while True:
#     with open("Orders.json", "r") as read:
#         orders = json.load(read)
#     # if len(orders["GBP_CAD"]["open"]) == 0:
#     if Other.timecheck("hour") == 60 or Other.timecheck("hour") == 30:
#         live("GBP_CAD")
# pairList = ["GBP_CAD"]
# print(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
# back()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
