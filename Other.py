from datetime import datetime, timedelta


def start():
    timezone = datetime.now() + timedelta(hours=4)
    hours = int(timezone.strftime("%H"))
    day = datetime.today().weekday()
    if day == 5:
        subtract = 240 + hours
    else:
        subtract = 336
    timesubtract = timezone - timedelta(hours=subtract)
    proper = timesubtract.strftime("%Y-%m-%dT%H:00:00Z")
    return proper


def converter(pp, val, pair):
    pip = {
        "GBP_AUD": 0.0001,
        "GBP_CAD": 0.0001
    }
    amount = float(val)
    if pp == "pip":
        base = pip[pair]
        return float(amount / base)
    elif pp == "price":
        base = pip[pair]
        return float(amount * base)
