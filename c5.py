import http.client,ssl,os
import json

from torch import obj

def readhashnames():
    names = set()
    with open("allitems.txt", "r", encoding="utf-8") as f:
        for line in f:
            names.add(line.strip())
    return names
def queryPrice(start,end):
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("openapi.c5game.com",context=context)
    app_key=os.getenv("C5_KEY")
    payload = json.dumps({
    "appId": 730,
    "marketHashNames": list(readhashnames())[start:end]
    })
    headers = {
    'Content-Type': 'application/json',
    }
    conn.request("POST", f"//merchant/market/v2/item/stat/hash/name?app-key={app_key}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    text = data.decode('utf-8', errors='replace')
    try:
        obj = json.loads(text)
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Non-JSON response:")
        print(text)

    return obj["data"]
def rentsort(data):

    items = [
        (k, v) for k, v in data.items()
        if v.get("temporaryRental") is not None and v.get("sellPrice") is not None and v.get("sellPrice")!=0
    ]

    sorted_items = sorted(
        items,
        key=lambda kv: kv[1]["temporaryRental"] / abs(kv[1]["sellPrice"]),
        reverse=True
    )

    for item in sorted_items:
        ratio = item[1]["temporaryRental"] / item[1]["sellPrice"]
        item[1]["ratio"] = ratio

    #print(sorted_items)
    for item in sorted_items:
        print(json.dumps(item[1], indent=2, ensure_ascii=False))
    
    with open("c5_rent_sort.json", "w+", encoding="utf-8") as f:
        for item in sorted_items:
            f.write(json.dumps(item[1],indent=2, ensure_ascii=False) + "\n")


#print(obj['data'])
def main():
    interval=100
    data={}
    for i in range(0,len(readhashnames()),interval):
        data=data|queryPrice(i,i+interval)
    rentsort(data)

main()