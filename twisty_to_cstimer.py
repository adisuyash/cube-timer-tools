# This script converts:
# - Converts Twisty Timer export data to csTimer-compatible JSON format,
# - Reads solves from Twisty Timer .txt file and outputs structured session data with metadata

import json
from datetime import datetime
from typing import Any

INPUT_FILE = "scrambles/twisty-timer.txt"
OUTPUT_FILE = "results/twisty-to-cstimer.json"


def parse_line(line: str):
    parts = line.strip().split(";")
    if len(parts) != 3:
        return None

    try:
        time_sec = float(parts[0].strip('"'))
        scramble = parts[1].strip('"')
        iso_date = parts[2].strip('"')

        return time_sec, scramble, iso_date
    except:
        return None


def normalize_solve(time_sec: float, scramble: str, iso_date: str):
    # convert seconds → milliseconds (int)
    time_ms = int(time_sec * 1000)

    # normalize scramble spacing
    scramble = " ".join(scramble.split())

    # convert ISO → UNIX timestamp
    dt = datetime.fromisoformat(iso_date)
    timestamp = int(dt.timestamp())

    return [[0, time_ms], scramble, "", timestamp]


def main():
    print("Running Twisty → csTimer conversion")

    session = []

    # Read Twisty file
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line)
            if not parsed:
                continue

            time_sec, scramble, iso_date = parsed
            solve = normalize_solve(time_sec, scramble, iso_date)
            session.append(solve)

    print(f"  Total solves converted: {len(session)}")

    # Build csTimer structure
    data: dict[str, Any] = {f"session{i}": [] for i in range(1, 16)}
    data["session1"] = session

    # minimal valid session metadata
    session_meta = {
        "1": {
            "name": 1,
            "opt": {"scrType": "222so"},
            "rank": 1
        }
    }

    data["properties"] = {
        "sessionData": json.dumps(session_meta),
        "scrType": "222so"
    }

    # Save output (JSON format)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))

    print(f"  Output written to: {OUTPUT_FILE}")
    print("Done.\n")


if __name__ == "__main__":
    main()