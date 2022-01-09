import json
import Indicators


# if bypass == 1 its a long if bypass == 2 its a short
import Other


def live5M(peaks, valleys, bypass=0):
    with open("JSON/5M.json", "r") as read:
        data5 = json.load(read)

    with open("JSON/15M.json", "r") as read:
        data15 = json.load(read)

    with open("JSON/1H.json", "r") as read:
        data1 = json.load(read)

    # long
    # check if 15 ema is higher than 60 ema
    if (float(data15[-2]["ema"]) > float(data1[-2]["ema"]) and bypass == 0) or bypass == 1:
        # check if the macd and signal lines are below the 0 line
        if (float(data5[-2]["macd"][0]) < 0) and (float(data5[-2]["macd"][1]) < 0) or bypass:
            # check if there is a bullish divergence (higher low on macd and lower low on price)
            if (data5[valleys[-1]["macd"][0]] > data5[valleys[-2]["macd"][0]]) and \
                    (data5[valleys[-1]]["mid"]["l"] < data5[valleys[-2]]["mid"]["l"]):
                # check if macd ever crosses above the 0 line
                sliced = data5[peaks[-1]:peaks[-2]]
                sliced.sort(key=lambda x: x["macd"][0], reverse=True)
                if sliced[0]["macd"][0] < 0:
                    # check if macd crosses over the signal line
                    if (data5[-3]["macd"][0] < data5[-2]["macd"][1]) and (data5[-3]["macd"][0] > data5[-2]["macd"][1]):
                        now = Other.current()
                        print("long ", now)
                        # place()
    # shorts
    # check if 15 ema is lower than 60 ema
    elif (float(data15[-2]["ema"]) < float(data1[-2]["ema"]) and bypass == 0) or bypass == 2:
        # check if the macd and signal lines are above the 0 line
        if (float(data5[-2]["macd"][0]) > 0) and (float(data5[-2]["macd"][1]) > 0) or bypass:
            # check if there is a bearish divergence (lower high on macd and higher high on price)
            if (data5[peaks[-1]["macd"][0]] < data5[peaks[-2]["macd"][0]]) and \
                    (data5[peaks[-1]]["mid"]["h"] > data5[peaks[-2]]["mid"]["h"]):
                # check if macd ever crosses below the 0 line
                sliced = data5[peaks[-1]:peaks[-2]]
                sliced.sort(key=lambda x: x["macd"][0])
                if sliced[0]["macd"][0] > 0:
                    # check if signal crosses over the macd line
                    if (data5[-3]["macd"][0] > data5[-2]["macd"][1]) and (data5[-3]["macd"][0] < data5[-2]["macd"][1]):
                        now = Other.current()
                        print("short ", now)
                        # place()


def place(pair, tp, sl, cur, time, lot="0.01"):
    with open("JSON/Orders.json", "r") as read:
        order = json.load(read)
    pair_list = {
        "GBP_CAD": []
    }
    if float(tp) > float(cur):
        order[pair]["open"].append(["buy", cur, sl, tp, time, lot])
    elif float(tp) < float(cur):
        order[pair]["open"].append(["sell", cur, sl, tp, time, lot])
    with open("JSON/Orders.json", "w") as out:
        out.write(json.dumps(order, indent=4))
    # mouse.position = pair_list[pair]
    # mouse.click(Button.left, 2)
    # keyboard.type("123")


# def modify(change):
#     if change == "be":
#         mouse.position = [123, 123]
#
#
# def watch(pair):
#     Indicators.dumpcur(pair)
#     now = datetime.now()
#     with open("Orders.json", "r") as read:
#         orders = json.load(read)
#     with open("cur.json", "r") as read:
#         cur = json.load(read)
#     bid = float(cur["prices"][0]["bids"][0]["price"])
#     asks = float(cur["prices"][0]["asks"][0]["price"])
#     for i in orders[pair]["open"]:
#         start = float(i[1])
#         if i[0] == "buy":
#             if bid > start + Other.converter("price", 10, pair):
#                 modify("be")
#         elif i[0] == "sell":
#             if asks < start - Other.converter("price", 10, pair):
#                 modify("be")