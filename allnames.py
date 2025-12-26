import requests
import time
import os

BASE_URL = "https://steamcommunity.com/market/search/render/"
OUTPUT_FILE = "cs2_market_hash_names.txt"
PROGRESS_FILE = "progress.txt"

params = {
    "appid": 730,
    "norender": 1,
    "count": 100
}

# 1️⃣ 读取已保存的 names
all_names = set()
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            all_names.add(line.strip())
    print(f"Loaded {len(all_names)} existing names.")

# 2️⃣ 读取进度
start = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        start = int(f.read().strip())
    print(f"Resuming from start={start}")

print("Start crawling...")

while True:
    try:
        params["start"] = start
        r = requests.get(BASE_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        results = data.get("results", [])
        total = data.get("total_count", 0)

        if not results:
            print("No more results. Finished.")
            break

        new_count = 0
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            for item in results:
                name = item["hash_name"]
                if name not in all_names:
                    f.write(name + "\n")
                    all_names.add(name)
                    new_count += 1
            f.flush()

        start += len(results)

        # 保存进度
        with open(PROGRESS_FILE, "w") as pf:
            pf.write(str(start))

        print(f"Fetched {start}/{total}, new added: {new_count}, total saved: {len(all_names)}")

        time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        print("Sleeping 10 seconds and retrying...")
        time.sleep(5)
        continue

print(f"Done. Total unique market_hash_name: {len(all_names)}")
