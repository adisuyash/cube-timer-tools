# Cube Timer File Formats
This document explains the file formats used by:

- [csTimer](#cstimer-format)
- [Twisty Timer](#twisty-timer-format)

and their [conversion logic](#conversion-mapping), which is used for vice-versa format conversion.

---

## csTimer Format

Structured JSON format used internally by csTimer to store solves and session metadata.

### File Type

- JSON (often saved as `.txt`)
- Structured data with sessions

### Top-Level Structure

```json
{
  "session1": [...],
  "session2": [],
  ...
  "session15": [],
  "properties": { ... }
}
```

### Solve Format

Each solve is an array with the following structure:

```json
[[penalty, time_ms], "SCRAMBLE", "COMMENT", timestamp]
```

### Fields:

- `penalty`
  - `0` → normal
  - `2000` → +2 seconds
  - `-1` → DNF

- `time_ms`
  - Integer (milliseconds)

- `SCRAMBLE`
  - String (space-separated moves)

- `COMMENT`
  - Usually empty string `""`

- `timestamp`
  - UNIX timestamp (seconds)

### Example Solve

```json
[[0, 12340], "R U R' F2 U2", "", 1773840000]
```

### Properties

```json
{
  "sessionData": "...",
  "scrType": "222so"
}
```

- `sessionData` is a JSON string (stringified JSON)
- `scrType` defines puzzle type
  - 2x2 - `222so`
  - 3x3 - `333`
  - 4x4 - `444wca`

### Sample File

To see an example of a csTimer file, check out: `[cstimer_sample.txt](cstimer_sample.txt)`

## Twisty Timer Format

Simple line-based text format used by Twisty Timer for exporting solves.

### File Type

- Plain text (`.txt`)
- One solve per line

### Line Format

```text
"time"; "scramble"; "ISO timestamp"
```

### Fields

- `time`
  - String (seconds, float)
  - Example: `"12.34"`

- `scramble`
  - String
  - Example: `"R U R' F2"`

- `timestamp`
  - ISO 8601 format
  - Includes timezone (e.g., `+05:30`)

### Example

```json
"20.39";"R F' R' U R' F U' R2 U R F'";"2026-03-07T17:13:45.643+05:30"
```

### Sample File

To see an example of a Twisty Timer file, check out: `[twisty_timer_sample.txt](twisty_timer_sample.txt)`

---

## Conversion Mapping

| Twisty Timer | csTimer                |
| ------------ | ---------------------- |
| seconds      | milliseconds (`×1000`) |
| ISO date     | UNIX timestamp         |
| scramble     | same                   |
| no penalty   | `[0, time_ms]`         |

---

### ⚠️ Important Rules

### csTimer:

- Must use integer milliseconds
- Must include sessions (1–15)
- Must be valid JSON

### Twisty:

- Must follow `"value";"value";"value"`
- Timestamp must be valid ISO format
