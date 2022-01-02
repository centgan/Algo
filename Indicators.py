import json
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import Other

idaccount = "101-002-19058958-001"
token = "ae2330665fa73fa2fe986faf62ffd895-2e75bde1f62ad95ada8ce0b42a77b557"
client = API(access_token = token)


def dumphis(instrument, gran, file):
    result = Other.start()
    param = {
            "from": result,
            "granularity": gran,
            "count": 5000
        }

    with open(file.format(instrument, gran), "w") as out:
        for i in InstrumentsCandlesFactory(instrument = instrument, params = param):
            client.request(i)
            out.write(json.dumps(i.response.get("candles"), indent = 4))


def dumpcur(instrument):
    params = {"instruments": instrument}
    r = pricing.PricingInfo(accountID=idaccount, params=params)

    with open("cur.json", "w") as out:
        client.request(r)
        out.write(json.dumps(r.response, indent=4))


def emahis():
    ema12, ema26 = [], []
    k = 2/13
    total = 0
    with open("5M.json", "r") as read:
        data = json.load(read)
    for i in range(len(data)):
        if i > 11:
            for j in range(i-12, i):
                total += float(data[j]["mid"]["c"])
            total = round(total/12, 7)
            if i == 12:
                ema12.append(total)
            else:
                e = float(data[i]["mid"]["c"]) * k
                em = ema12[-1] * (1-k)
                fin = round(e + em, 6)
                ema12.append(fin)
                data[i].__setitem__("ema12", fin)
    total = 0
    k = 2/27
    for i in range(len(data)):
        if i > 25:
            for j in range(i-26, i):
                total += float(data[j]["mid"]["c"])
            total = round(total/26, 7)
            if i == 26:
                ema26.append(total)
            else:
                e = float(data[i]["mid"]["c"]) * k
                em = ema26[-1] * (1-k)
                fin = round(e + em, 6)
                ema26.append(fin)
                data[i].__setitem__("ema26", fin)
    with open("5M.json", "w") as out:
        out.write(json.dumps(data, indent=4))


def emaTime(file):
    ema = []
    k = 2 / 51
    total = 0
    with open(file, "r") as read:
        data = json.load(read)

    for i in range(len(data)):
        if i > 49:
            for j in range(i-50, i):
                total += float(data[j]["mid"]["c"])
            total = round(total/50, 7)
            if i == 50:
                ema.append(total)
            else:
                e = float(data[i]["mid"]["c"]) * k
                em = ema[-1] * (1-k)
                fin = round(e + em, 6)
                ema.append(fin)
                data[i].__setitem__("ema", fin)

    with open(file, "w") as out:
        out.write(json.dumps(data, indent=4))


def machis():
    emahis()
    # mc = []
    k = 2/10
    total = 0
    with open("5M.json", "r") as read:
        data = json.load(read)
    for i in range(27, len(data)):
        ema12 = float(data[i]["ema12"])
        ema26 = float(data[i]["ema26"])
        macd = round(ema12 - ema26, 6)
        # mc.append(macd)
        data[i].__setitem__("macd", [macd])
        if i > 35:
            if i == 36:
                for j in range(i-8, i+1):
                    total += float(data[j]["macd"][0])
                total = round(total/9, 7)
                data[i]["macd"].append(total)
            else:
                s = float(data[i]["macd"][0]) * k
                si = float(data[i-1]["macd"][1]) * (1-k)
                fin = round(s + si, 6)
                data[i]["macd"].append(fin)
    with open("5M.json", "w") as out:
        out.write(json.dumps(data, indent=4))


def atrhis():
    with open("5M.json", "r") as read:
        data = json.load(read)
    largest = []
    for i in range(len(data)):
        if i > 0:
            first = float(data[i]["mid"]["h"]) - float(data[i]["mid"]["l"])
            second = abs(float(data[i]["mid"]["h"]) - float(data[i-1]["mid"]["c"]))
            third = abs(float(data[i]["mid"]["l"]) - float(data[i-1]["mid"]["c"]))
            true = [first, second, third]
            true.sort()
            largest.append(true[-1])
            # print(largest)
            if i > 13:
                total = 0
                for j in range(i-14, i):
                    total += largest[j]
                total = round(total/14, 6)
                total = round(total - 0.00005, 6)
                # print(total)
                data[i].__setitem__("atr", total)
    with open("5M.json", "w") as out:
        out.write(json.dumps(data, indent=4))


def cmfhis():
    mfl = []
    with open("5M.json", "r") as read:
        data = json.load(read)
    for i in range(len(data)):
        m = float(data[i]["mid"]["c"]) - float(data[i]["mid"]["l"])
        mf = float(data[i]["mid"]["h"]) - float(data[i]["mid"]["c"])
        mfb = float(data[i]["mid"]["h"]) - float(data[i]["mid"]["l"])
        mfm = (m - mf)/mfb
        mfv = round(mfm * float(data[i]["volume"]), 6)
        mfl.append(mfv)
        if i > 19:
            money = 0
            vol = 0
            for j in range(i-19, i+1):
                money += mfl[j]
                vol += float(data[j]["volume"])
            # print(money, vol, data[i]["time"])
            cmf = round(money / vol, 6)
            data[i].__setitem__("cmf", cmf)
    with open("5M.json", "w") as out:
        out.write(json.dumps(data, indent=4))
    # print(mfl)


def supres():
    suplist = []
    reslist = []
    with open("5M.json", "r") as read:
        data = json.load(read)
    for i in range(len(data)):
        if (i > 1) and (i < len(data)-1):
            if (float(data[i-1]["mid"]["h"]) < float(data[i]["mid"]["h"])) and (float(data[i+1]["mid"]["h"]) < float(data[i]["mid"]["h"])):
                # reslist.append(data[i+1]["mid"]["h"])
                reslist.append(i+1)
            elif (float(data[i-1]["mid"]["l"]) > float(data[i]["mid"]["l"])) and (float(data[i+1]["mid"]["l"]) > float(data[i]["mid"]["l"])):
                # suplist.append(data[i+1]["mid"]["l"])
                suplist.append(i+1)

    # suplist.sort()
    # reslist.sort()
    # for i in suplist:
    #     for j in suplist:
    #         if float(i) +

    return suplist, reslist


