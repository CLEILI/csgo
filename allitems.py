import requests

url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/all.json"

resp = requests.get(url, timeout=15)
resp.raise_for_status()          # raise error if HTTP != 200
data = resp.json()               # parse JSON into dict/list

print(type(data))

with open("allitems.txt", "w+", encoding="utf-8") as f:
    for k,v in data.items():
        if isinstance(v, dict) and 'market_hash_name' in v:
            print(v['market_hash_name'])
            if v['market_hash_name'] is not None:
                f.write(str(v['market_hash_name']) + "\n")