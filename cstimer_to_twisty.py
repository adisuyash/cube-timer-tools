# This script converts:
# - csTimer export data into a format compatible with Twisty Timer,
# - then merges it with existing Twisty Timer data while removing duplicates.

import json
from datetime import datetime, timezone, timedelta
import random
import re
import os

# FILES
INPUT_CSTIMER = "scrambles/cstimer.txt"
INPUT_TWISTY = "scrambles/twisty-timer.txt"

TEMP_FILE = "temp/dedup-ready.txt"
OUTPUT_FILE = "results/cstimer-to-twisty.txt"

IST = timezone(timedelta(hours=5, minutes=30))

# ensure folders exist
os.makedirs("temp", exist_ok=True)
os.makedirs("results", exist_ok=True)


# -----------------------------
# STEP 1: Convert csTimer
# -----------------------------
def convert_cstimer():
    print("\n[1/2] Converting csTimer data...")

    with open(INPUT_CSTIMER, "r", encoding="utf-8") as f:
        raw = f.read()

        # remove trailing commas before ] or }
        cleaned = re.sub(r",\s*([\]}])", r"\1", raw)

        try:
            data = json.loads(cleaned)
        except Exception as e:
            print("ERROR: Failed to parse csTimer JSON")
            raise e

    solves = data.get("session1", [])
    print(f"  Total solves found: {len(solves)}")

    formatted = []

    for solve in solves:
        try:
            time_ms = solve[0][1]
            scramble = " ".join(solve[1].split())
            timestamp = solve[3]

            time_sec = round(time_ms / 1000, 2)
            dt = datetime.fromtimestamp(timestamp, IST)

            ms = random.randint(0, 999)
            date_iso = dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms:03d}+05:30")

            line = f"\"{time_sec}\";\"{scramble}\";\"{date_iso}\""
            formatted.append(line)

        except Exception:
            print(f"  Skipped invalid solve: {solve}")

    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted))

    print(f"  Output written to: {TEMP_FILE}")


# -----------------------------
# STEP 2: Merge + Dedup
# -----------------------------
def normalize_scramble(scramble):
    return " ".join(scramble.split())


def parse_line(line):
    line = line.strip()
    if not line:
        return None

    parts = line.split(";")
    if len(parts) != 3:
        return None

    scramble = normalize_scramble(parts[1].strip().strip('"'))
    return scramble, line


def merge_and_dedup():
    print("\n[2/2] Merging and deduplicating...")

    existing_scrambles = set()
    final_lines = []

    # Load Twisty
    with open(INPUT_TWISTY, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line)
            if parsed:
                scramble, original_line = parsed
                if scramble not in existing_scrambles:
                    existing_scrambles.add(scramble)
                    final_lines.append(original_line)

    print(f"  Existing unique scrambles: {len(existing_scrambles)}")

    added = 0

    # Add csTimer
    with open(TEMP_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line)
            if not parsed:
                continue

            scramble, original_line = parsed

            if scramble not in existing_scrambles:
                existing_scrambles.add(scramble)
                final_lines.append(original_line)
                added += 1

    print(f"  New unique scrambles added: {added}")
    print(f"  Final total scrambles: {len(final_lines)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_lines))

    print(f"  Output written to: {OUTPUT_FILE}")


# -----------------------------
# RUN PIPELINE
# -----------------------------
def main():
    print("Running csTimer → Twisty pipeline")

    convert_cstimer()
    merge_and_dedup()

    print("\nDone.\n")


if __name__ == "__main__":
    main()