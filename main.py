# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Indicators
import Orders
import Other
import json
from datetime import datetime, timedelta
import pynput
from pynput.mouse import Button, Controller
# from pynput.keyboard import Key, Controller
import numpy as np
from scipy.signal import find_peaks

mouse = Controller()
# keyboard = Controller()


while True:
    now = Other.current()
    now = int(datetime.strptime(now, "%H:%M:%S").time().minute)
    if now == 00:
        Indicators.dumphis("GBP_USD", "M5", "JSON/5M.json")
        Indicators.dumphis("GBP_USD", "M15", "JSON/15M.json")
        Indicators.dumphis("GBP_USD", "H1", "JSON/1H.json")
        mac = Indicators.machis()
        reverse = mac * -1
        peak = find_peaks(mac)[0]
        valley = find_peaks(reverse)[0]
        order = Orders.live5M(peak, valley)
        print(order)
    elif now % 15 == 0:
        Indicators.dumphis("GBP_USD", "M5", "JSON/5M.json")
        Indicators.dumphis("GBP_USD", "M15", "JSON/15M.json")
        mac = Indicators.machis()
        reverse = mac * -1
        peak = find_peaks(mac)[0]
        valley = find_peaks(reverse)[0]
        order = Orders.live5M(peak, valley)
        print(order)
    elif now % 5 == 0:
        Indicators.dumphis("GBP_USD", "M5", "JSON/5M.json")
        mac = Indicators.machis()
        reverse = mac * -1
        peak = find_peaks(mac)[0]
        valley = find_peaks(reverse)[0]
        order = Orders.live5M(peak, valley)
        print(order)
    print("works")


# Indicators.dumphis("GBP_USD", "M5", "JSON/5M.json")
# # Indicators.dumphis("GBP_USD", "M15", "15M.json")
# # Indicators.dumphis("GBP_USD", "H1", "1H.json")
# mac = Indicators.machis()
#
# # reverse = mac*-1
# peak = find_peaks(mac)[0]
# # valley = find_peaks(reverse)[0]
# # print(peak)
# # print(valley)
# with open("JSON/5M.json", "r") as read:
#     data5 = json.load(read)
#
# print(peak)
# # print(peak[-1])
# sliced = data5[peak[-2]:peak[-1]]
# print(sliced)
# sliced.sort(key=lambda x: x["macd"][0])
# print(sliced)



# Indicators.emaTime("1H.json")
# Indicators.emaTime("15M.json")


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
