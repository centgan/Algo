# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Indicators
import Other
import json
from datetime import datetime
import pynput
from pynput.mouse import Button
from pynput.keyboard import Key, Controller

mouse = pynput.mouse.Controller()
keyboard = Controller()


def back():
    con3 = False
    Indicators.dumpcur("GBP_CAD")
    Indicators.dumphis("GBP_CAD", "M30")
    Indicators.machis()
    Indicators.atrhis()
    Indicators.cmfhis()
    with open("Historicaldata.json", "r") as read:
        data = json.load(read)
    with open("cur.json", "r") as read:
        cur = json.load(read)
    # buys are bid
    # sells are asks
    bid = float(cur["prices"][0]["bids"][0]["price"])
    asks = float(cur["prices"][0]["asks"][0]["price"])
    for i in range(46, len(data)):
        if float(data[i]["macd"][0]) > 0 and float(data[i]["macd"][1]) > 0:
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
        elif float(data[i]["macd"][0]) < 0 and float(data[i]["macd"][1]) < 0:
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
    proper = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open("Historicaldata.json", "r") as read:
        data = json.load(read)
    with open("cur.json", "r") as read:
        cur = json.load(read)
    with open("Orders.json", "r") as read:
        orders = json.load(read)
    # buys are bid
    # sells are asks
    bid = float(cur["prices"][0]["bids"][0]["price"])
    asks = float(cur["prices"][0]["asks"][0]["price"])

    if len(orders[pair]["open"]) == 0:
        if Other.timecheck("hour") == 60 or Other.timecheck("hour") == 30:
            Indicators.dumpcur(pair)
            Indicators.dumphis(pair, "M30")
            Indicators.machis()
            Indicators.atrhis()
            Indicators.cmfhis()
            if float(data[-2]["macd"][0]) > 0 and float(data[-2]["macd"][1]) > 0:
                con1 = float(data[-3]["macd"][0]) < float(data[-3]["macd"][1])
                con2 = float(data[-2]["macd"][0]) > float(data[-2]["macd"][1])
                if float(data[-2]["cmf"]) > 0:
                    con3 = True
                elif float(data[-2]["cmf"]) == 0 and float(data[-2]["cmf"]) > 0:
                    con3 = True
                else:
                    con3 = False
                if con1 and con2 and con3:
                    # place the order, possibly create a new function to do this
                    place()
                    print("buy", proper, data[-1]["atr"])
                elif float(data[-3]["macd"][0]) < 0 or float(data[-3]["macd"][1]) < 0:
                    # place the order, possibly create a new function to do this
                    place()
                    print("buy", proper, data[-1]["atr"])
            elif float(data[-2]["macd"][0]) < 0 and float(data[-2]["macd"][1]) < 0:
                con1 = float(data[-3]["macd"][0]) > float(data[-3]["macd"][1])
                con2 = float(data[-2]["macd"][0]) < float(data[-2]["macd"][1])
                if float(data[-2]["cmf"]) < 0:
                    con3 = True
                elif float(data[-2]["cmf"]) == 0 and float(data[-2]["cmf"]) < 0:
                    con3 = True
                else:
                    con3 = False
                if con1 and con2 and con3:
                    # place the order, possibly create a new function to do this
                    print("sell", proper, data[-1]["atr"])
                    print("sell", proper, data[-1]["atr"])
                elif float(data[-3]["macd"][0]) > 0 or float(data[-3]["macd"][1]) > 0:
                    # place the order, possibly create a new function to do this
                    place()
                    print("sell", proper, data[-1]["atr"])
    else:
        watch()


def place():
    pair_list = {
        "GBP_CAD": []
    }
    mouse.position = [2130, 742]
    mouse.click(Button.left, 2)
    keyboard.type("123")


def watch():
    pass


def init():
    Indicators.dumpcur("GBP_CAD")
    Indicators.dumphis("GBP_CAD", "M30")
    Indicators.machis()
    Indicators.atrhis()
    Indicators.cmfhis()


# pairList = ["GBP_CAD"]
# print(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
# back()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
