# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Indicators
import Other
import json


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


back()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
