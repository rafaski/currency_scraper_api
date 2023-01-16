from datetime import datetime

history = [
    {
        "source": "GBP",
        "target": "EUR",
        "value": 1.14705,
        "time": 1671307200000
    },
    {
        "source": "GBP",
        "target": "EUR",
        "value": 1.14705,
        "time": 1671310800000
    },
    {
        "source": "GBP",
        "target": "EUR",
        "value": 1.14705,
        "time": 1671314400000
    }
]

a = history[0]["time"]
b = history[1]["time"]

print(datetime.fromtimestamp(a/1000.0))
print(datetime.fromtimestamp(b/1000.0))

rates = [
    {
        "rate": 1.12695,
        "source": "GBP",
        "target": "EUR",
        "time": "2023-01-16T21:13:22+0000"
    }
]

datetime_str = rates[0]["time"]
datetime_object = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S+0000")

print(datetime_object)
