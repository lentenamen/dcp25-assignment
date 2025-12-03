import pandas as pd

def load_abc_file(filename: str):
    """Load ABC file into list of lines"""
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def parse_tune(tune_lines: list[str]) -> dict:
    """Parse a single tune into a dictionary with features + notation"""
    tune = {
        'id': None,       # X: reference number
        'title': None,    # T: first title only
        'rhythm': None,   # R:
        'meter': None,    # M:
        'key': None,      # K:
        'tempo': None,    # Q:
        'source': None,   # S:
        'notation': ""    # all note lines after K:
    }

    tune_started = False
    notation_lines = []

    for line in tune_lines:
        raw = line.strip()
        if not raw and not tune_started:
            continue

        if raw.startswith("X:"):
            tune['id'] = raw[2:].strip()
        elif raw.startswith("T:") and tune['title'] is None:
            tune['title'] = raw[2:].strip()
        elif raw.startswith("R:"):
            tune['rhythm'] = raw[2:].strip().lower()
        elif raw.startswith("M:"):
            tune['meter'] = raw[2:].strip()
        elif raw.startswith("K:"):
            tune['key'] = raw[2:].strip()
            tune_started = True
        elif raw.startswith("Q:"):
            tune['tempo'] = raw[2:].strip()
        elif raw.startswith("S:"):
            tune['source'] = raw[2:].strip()
        elif body_started:
            notation_lines.append(raw)

    tune['notation'] = "\n".join(notation_lines)
    return tune

def parse_all_tunes(lines: list[str]) -> list[dict]:
    """Parse all tunes from lines"""
    tunes = []
    current_tune_lines = []

    for line in lines:
        line = line.rstrip()
        if line.startswith("X:") and current_tune_lines:
            tunes.append(parse_tune(current_tune_lines))
            current_tune_lines = []
        current_tune_lines.append(line)

    if current_tune_lines:
        tunes.append(parse_tune(current_tune_lines))

    print(f"Parsed {len(tunes)} tunes")
    return tunes

# === Example usage ===
lines = load_abc_file('abc_books/1/hnair0.abc')
tunes = parse_all_tunes(lines)

df = pd.DataFrame(tunes)

# Show metadata
print(df[['id','title','rhythm','meter','key','tempo','source']].head())

# Show notation preview
print("\nNotation preview (first 10 lines of tune 1):\n")
print("\n".join(df.loc[0, 'notation'].splitlines()[:10]))
