from datetime import datetime, timedelta


def start():
    timezone = datetime.now() + timedelta(hours=4)
    hours = int(timezone.strftime("%H"))
    day = datetime.today().weekday()
    if day == 5:
        subtract = 240 + hours
    else:
        subtract = 168
    timesubtract = timezone - timedelta(hours=subtract)
    proper = timesubtract.strftime("%Y-%m-%dT%H:00:00Z")
    return proper


def current():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def converter(pp, val, pair):
    pip = {
        "GBP_AUD": 0.0001,
        "GBP_CAD": 0.0001,
        "EUR_CAD": 0.0001
    }
    amount = float(val)
    if pp == "pip":
        base = pip[pair]
        return float(amount / base)
    elif pp == "price":
        base = pip[pair]
        return float(amount * base)


def timecheck(forback):
    time = datetime.now()
    new = time + (datetime.min - time) % timedelta(minutes = 30)
    hourly = time + (datetime.min - time) % timedelta(minutes = 60)
    hourlystrip = str(hourly - time).lstrip("0:")
    almosthour = hourlystrip[:len(hourlystrip) - 10]
    final = str(new - time).lstrip("0:")
    almost = final[:len(final) - 10]
    if forback == "forward":
        return float(almost) + 1
    elif forback == "back":
        return 30 - (float(almost) + 1)
    elif forback == "start":
        rounded = time - (time - datetime.min) % timedelta(minutes=30)
        return rounded.strftime("%Y-%m-%dT%H:%M:00Z")
    elif forback == "hour":
        return float(almosthour) + 1

