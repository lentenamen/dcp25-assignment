import pandas as pd
import os
import sqlite3
import tkinter as tk
from tkinter import ttk

# --- ABC Parsing ---
def load_abc_file(filename: str):
    #Load ABC file into list of lines
    # 'errors=replace' prevents crashes if bad characters exist
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def parse_tune(tune_lines: list[str], book_number: int) -> dict:
    #Parse a single tune into a dictionary with features + notation
    tune = {
        'id': None,       # X: reference number
        'title': None,    # T: first title only
        'alt_titles' :[], # T: extra T lines
        'rhythm': None,   # R:
        'meter': None,    # M:
        'key': None,      # K:
        'tempo': None,    # Q:
        'source': None,   # S:
        'notation': "",    # all note lines after K:
        'book_number': book_number
    }
    tune_started = False
    notation_lines = []

    # Loop through each line in the tune
    for line in tune_lines:
        raw = line.strip()
        # Ignore empty lines before the tune starts
        if not raw and not tune_started:
            continue
        if raw.startswith("X:"):
            tune['id'] = raw[2:].strip()
        elif raw.startswith("T:"):
            title_text = raw[2:].strip()
            if tune['title'] is None:
                tune['title'] = title_text
            else:
                tune['alt_titles'].append(title_text)
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
            # All remaining lines after K: are musical notes
            notation_lines.append(raw)

    # Combine all music notation lines into one block
    tune['notation'] = "\n".join(notation_lines)
    return tune

def parse_all_tunes(lines: list[str], book_number: int) -> list[dict]:
    #Parse all tunes from lines in a file
    tunes = []
    current_tune_lines = []
    for line in lines:
        line = line.rstrip()
        if line.startswith("X:") and current_tune_lines:
            tunes.append(parse_tune(current_tune_lines, book_number))
            current_tune_lines = []
        current_tune_lines.append(line)
    if current_tune_lines:
        tunes.append(parse_tune(current_tune_lines, book_number))
    return tunes

def process_file(file_path: str, book_number: int) -> list[dict]:
    #Helper to load and parse a single ABC file
    lines = load_abc_file(file_path)
    return parse_all_tunes(lines, book_number)

def load_abc_files(root_folder: str) -> pd.DataFrame:
    #Load all ABC files from numbered subfolders into a DataFrame
    all_tunes = []
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)
        # Each folder represents a different book number
        if os.path.isdir(item_path) and item.isdigit():
            book_number = int(item)  # starts at 0
            print(f"Found numbered directory: {item}")
            for file in os.listdir(item_path):
                if file.endswith('.abc'):
                    file_path = os.path.join(item_path, file)
                    print(f"  Found abc file: {file}")
                    tunes = process_file(file_path, book_number)
                    all_tunes.extend(tunes)
    # Convert all collected tunes into a DataFrame
    df = pd.DataFrame(all_tunes)
    print(f"\nLoaded {len(df)} tunes from {root_folder}")
    return df

# --- Analysis Functions ---
def get_tunes_by_book(df: pd.DataFrame, book_number: int) -> pd.DataFrame:
    #Get all tunes from a specific book
    return df[df['book_number'] == book_number]

def get_tunes_by_type(df: pd.DataFrame, tune_type: str) -> pd.DataFrame:
    #Get all tunes of a specific rhythm/type
    return df[df['rhythm'].str.lower() == tune_type.lower()]

def search_tunes(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    #Search tunes by title (case insensitive)
    return df[df['title'].str.contains(search_term, case=False, na=False)]

# --- Database Setup ---
df = load_abc_files("abc_books")
tunes = df.to_dict(orient="records")

#function calling
print("\n5 from Book 1 ")
print(get_tunes_by_book(df, 1)[["id", "title"]].head(5))

print("\n5 Reel Tunes")
print(get_tunes_by_type(df, "reel")[["id", "title", "rhythm"]].head(5))

print("\nSearch Results for 'boyle'")
print(search_tunes(df, "boyle")[["id", "title"]].head(5))

# Create SQLite database
conn = sqlite3.connect("abc_tunes.db")
cursor = conn.cursor()

# Create database table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tunes (
    id TEXT PRIMARY KEY,
    title TEXT,
    alt_titles TEXT,
    rhythm TEXT,
    meter TEXT,
    key TEXT,
    tempo TEXT,
    source TEXT,
    notation TEXT,
    book_number INTEGER
)
""")

# Insert all tunes into the database
for tune in tunes:
    cursor.execute("""
    INSERT OR REPLACE INTO tunes (id, title, alt_titles, rhythm, meter, key, tempo, source, notation, book_number)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        tune['id'] or "",
        tune['title'] or "",
        ", ".join(tune['alt_titles']),
        tune['rhythm'] or "",
        tune['meter'] or "",
        tune['key'] or "",
        tune['tempo'] or "",
        tune['source'] or "",
        tune['notation'] or "",
        tune['book_number']
    ))
# Save database changes
conn.commit()

# --- Tkinter GUI ---
root = tk.Tk()
root.title("ABC Tunes Viewer")
root.geometry("1000x650")

# Top controls
top = tk.Frame(root, padx=5, pady=5)
top.pack(fill="x")

tk.Label(top, text="Search:").pack(side="left")
search_entry = tk.Entry(top, width=25)
search_entry.pack(side="left", padx=5)

tk.Label(top, text="Sort by:").pack(side="left", padx=(10, 0))
sort_var = tk.StringVar(value="title")
sort_menu = tk.OptionMenu(top, sort_var, "title", "rhythm", "meter", "key", "tempo", "source", "book_number")
sort_menu.pack(side="left", padx=5)

def load_data(query="", sort_col=None):
    # Clears and reloads table data based on filter and sort selection
    for row in tree.get_children():
        tree.delete(row)
    sql = """SELECT book_number, id, title, alt_titles, rhythm, meter, key, tempo, source 
             FROM tunes"""
    params = []
    if query:
        q = f"%{query}%"
        sql += """ WHERE title LIKE ? 
                   OR alt_titles LIKE ? 
                   OR rhythm LIKE ? 
                   OR key LIKE ?"""
        params = [q, q, q, q]
    if sort_col:
        sql += f" ORDER BY {sort_col} COLLATE NOCASE"
    for row in cursor.execute(sql, params):
        tree.insert("", "end", values=row)

tk.Button(top, text="Filter", command=lambda: load_data(search_entry.get().strip(), sort_var.get())).pack(side="left", padx=5)
tk.Button(top, text="Clear", command=lambda: (search_entry.delete(0, tk.END), load_data())).pack(side="left")

# Table
cols = ("Book", "ID", "Title", "Alt Titles", "Rhythm", "Meter", "Key", "Tempo", "Source")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=110)
tree.pack(fill="both", expand=True)

# Details
details = tk.Text(root, wrap="word", height=10)
details.pack(fill="both", expand=True)

def show_details(_):
    # Displays full tune information when a row is selected
    selected = tree.selection()
    if not selected:
        return
    tune_id = tree.item(selected[0])["values"][1]
    tune = cursor.execute("SELECT * FROM tunes WHERE id=?", (tune_id,)).fetchone()
    if tune:
        details.delete("1.0", tk.END)
        details.insert(tk.END, "\n".join([
            f"ID: {tune[0]}",
            f"Title: {tune[1]}",
            f"Alt Titles: {tune[2]}",
            f"Rhythm: {tune[3]}",
            f"Meter: {tune[4]}",
            f"Key: {tune[5]}",
            f"Tempo: {tune[6]}",
            f"Source: {tune[7]}",
            f"Notation:\n{tune[8]}",
            f"Book: {tune[9]}"
        ]))

tree.bind("<<TreeviewSelect>>", show_details)# Bind table clicks to the detail viewer

load_data()# Load all data initially
root.mainloop()# Start the GUI application loop
conn.close()# Close the database connection