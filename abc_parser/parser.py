import pandas as pd
import os

def load_abc_file(filename: str):
    #Load ABC file into list of lines
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def parse_tune(tune_lines: list[str]) -> dict:
    #Parse a single tune into a dictionary with features + notation
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
        elif tune_started:
            notation_lines.append(raw)

    tune['notation'] = "\n".join(notation_lines)
    return tune

def parse_all_tunes(lines: list[str]) -> list[dict]:
    #Parse all tunes from lines
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

    return tunes

def process_file(file_path: str) -> list[dict]:
    #Helper to load and parse a single ABC file
    lines = load_abc_file(file_path)
    return parse_all_tunes(lines)

def load_abc_files(root_folder: str) -> pd.DataFrame:
    all_tunes = []

    # Iterate over items in the root books_dir
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)

        # Only look at numbered subdirectories
        if os.path.isdir(item_path) and item.isdigit():
            print(f"Found numbered directory: {item}")

            # Iterate over files in that directory
            for file in os.listdir(item_path):
                if file.endswith('.abc'):
                    file_path = os.path.join(item_path, file)
                    print(f"  Found abc file: {file}")

                    # Parse this file and extend the master list
                    tunes = process_file(file_path)
                    all_tunes.extend(tunes)

    df = pd.DataFrame(all_tunes)
    print(f"\nLoaded {len(df)} tunes from {root_folder}")
    return df

# === Example usage ===
lines = load_abc_file('abc_books/1/hnair0.abc')
tunes = parse_all_tunes(lines)
df = pd.DataFrame(tunes)

df = load_abc_files("abc_books")
print(df[['id','title','rhythm','meter','key','tempo','source']].head())
