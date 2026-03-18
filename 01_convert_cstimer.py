# Converts cstimer.txt to a format ready for deduplication.

import json
from datetime import datetime, timezone, timedelta
import random

INPUT_FILE = "scrambles/cstimer.txt" # input file from cstimer.net export
OUTPUT_FILE = "temp/dedup-ready.txt" # output file in the format "time;scramble;date" ready for deduplication with twisty-timer.txt
SKIP = 0

IST = timezone(timedelta(hours=5, minutes=30))

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    solves = data["session1"]

    print(f"📊 Total solves: {len(solves)}")

    formatted = []

    for solve in solves[SKIP:]:
        try:
            time_ms = solve[0][1]
            scramble = " ".join(solve[1].split())  # normalize
            timestamp = solve[3]

            time_sec = round(time_ms / 1000, 2)

            dt = datetime.fromtimestamp(timestamp, IST)

            ms = random.randint(0, 999)

            date_iso = dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms:03d}+05:30")

            line = f"\"{time_sec}\";\"{scramble}\";\"{date_iso}\""

            formatted.append(line)

        except Exception:
            print("⚠️ Skipped:", solve)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted))

    print(f"\n✅ DONE → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()