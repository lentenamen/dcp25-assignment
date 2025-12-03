import pandas as pd

# Part 2: Read file
def load_abc_file(filename):
    """Load ABC file into list of lines"""
    with open(filename, 'r', encoding='latin-1') as f:
        lines = f.readlines()

        print(f"Number of lines : {len(lines)}")

        print("first 20 lines:")
        for line in lines[:20]:
            print(line.rstrip())

        print("last 10 lines:")
        for line in lines[-10:]:
            print(line.strip())
    return lines

# Part 3: Parse tunes
def parse_tune(tune_lines):
    """Parse a single tune from lines"""
    tune = {
        'X': None,
        'title': None,
        'alt_title': [],
        'tune_type': None,
        'key': None,
        'notation': '\n'.join(tune_lines)
    }

    title_count = 0
    
    for line in tune_lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("X:"):
            tune['X'] = line[2:].strip()
        elif line.startswith("T:"):
            title_count += 1
            if title_count == 1:
                tune['title'] = line[2:].strip()
            else:
                tune['alt_title'].append(line[2:].strip())
        elif line.startswith("R:"):
            tune['tune_type'] = line[2:].strip()
        elif line.startswith("K:"):
            tune['key'] = line[2:].strip()

    return tune



def parse_all_tunes(lines):
    """Parse all tunes from lines"""
    tunes = []
    current_tune_lines = []
    blank_count = 0

    for line in lines:
        line = line.rstrip()

        if not line.strip():
            blank_count = blank_count + 1

        if line.startswith("X:"):
            if current_tune_lines:
                tune = parse_tune(current_tune_lines)
                tunes.append(tune)
                current_tune_lines = []

        current_tune_lines.append(line)

    if current_tune_lines:
        tune = parse_tune(current_tune_lines)
        tunes.append(tune)

    #test
    print(f"\nFound {blank_count} blank lines")
    print(f"\nFound {len(tunes)} tunes")
    print("\nFirst tune:")
    print(tunes[1])
    print("\nLast tune:")
    print(tunes[-1])   
    
    return tunes

# Load file
lines = load_abc_file('data/oneills.abc')
print(f"Loaded {len(lines)} lines")
    
# Parse tunes
tunes = parse_all_tunes(lines)
print(f"Parsed {len(tunes)} tunes")

#part 4   
# Create DataFrame
df = pd.DataFrame(tunes)

# Print basic info
print(df.shape)
print(df.head())
print(df.info())

# Check for missing values
print(df.isnull().sum())

# What columns do we have?
print(df.columns)
    
# Analysis
print("\n=== TUNE TYPE COUNTS ===")
# TODO: Your code here
print("Amount of tunes")
print(df['tune_type'].value_counts())
    
print("\n=== KEY COUNTS ===")
# TODO: Your code here
print(df['key'].value_counts())
    
print("\n=== ALCOHOLIC DRINKS IN TITLES ===")
# TODO: Your code here
alcohol = df['title'].str.contains(r'\bwhiskey\b|\bbrandy\b|\bbeer\b|\bale\b|\bwine\b|\bwhisky\b|\bpunch\b|\bporter\b|\brum\b|\bgin\b', case=False, na=False)
print(f"There are {alcohol.sum()} tunes mentioning alcohol")
print(df.loc[alcohol, ['X', 'title']])
df.to_csv('parsed_tunes.csv', index=False)