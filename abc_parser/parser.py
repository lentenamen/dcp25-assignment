import pandas as pd
import os
import sqlite3
import tkinter as tk
from tkinter import ttk

def load_abc_file(filename: str):
    #Load ABC file into list of lines
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        return f.readlines()

def parse_tune(tune_lines: list[str]) -> dict:
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

df = load_abc_files("abc_books")

#print(df[['id','title','rhythm','meter','key','tempo','source','alt_titles']].head())
# Convert DataFrame rows into list of dicts
tunes = df.to_dict(orient="records")

# Connect to SQLite
conn = sqlite3.connect("abc_tunes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tunes (
    id TEXT KEY,
    title TEXT,
    alt_titles TEXT,
    rhythm TEXT,
    meter TEXT,
    key TEXT,
    tempo TEXT,
    source TEXT,
    notation TEXT
)
""")

# Insert parsed tunes
for tune in tunes:
    cursor.execute("""
    INSERT OR REPLACE INTO tunes (id, title, alt_titles, rhythm, meter, key, tempo, source, notation)
    VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        tune['id'] or "",        
        tune['title'] or "",
        ", ".join(tune['alt_titles']),
        tune['rhythm'] or "",
        tune['meter'] or "",
        tune['key'] or "",
        tune['tempo'] or "",
        tune['source'] or "",
        tune['notation'] or ""
    ))

conn.commit()
rows = cursor.fetchall()
for row in rows:
    print(row)

print("Done inserting", len(tunes), "tunes")
# --- Tkinter GUI ---
root = tk.Tk()
root.title("ABC Tunes Viewer")
root.geometry("900x600")

# Search + Sort controls
top = tk.Frame(root, padx=5, pady=5)
top.pack(fill="x")

search_entry = tk.Entry(top, width=30)
search_entry.pack(side="left", padx=5)

def load_data(query="", sort_col=None):
    for row in tree.get_children():
        tree.delete(row)
    sql = "SELECT id,title,alt_titles,rhythm,meter,key,tempo,source FROM tunes"
    params = []
    if query:
        q = f"%{query}%"
        sql += " WHERE title LIKE ? OR alt_titles LIKE ? OR rhythm LIKE ? OR key LIKE ?"
        params = [q,q,q,q]
    if sort_col:
        sql += f" ORDER BY {sort_col} COLLATE NOCASE"
    for row in cursor.execute(sql, params):
        tree.insert("", "end", values=row)

def filter_data():
    load_data(search_entry.get().strip(), sort_var.get())

def clear_filter():
    search_entry.delete(0, tk.END)
    load_data()

tk.Button(top, text="Filter", command=filter_data).pack(side="left")
tk.Button(top, text="Clear", command=clear_filter).pack(side="left", padx=5)

sort_var = tk.StringVar(value="title")
sort_menu = tk.OptionMenu(top, sort_var, "title","rhythm","meter","key","tempo","source")
sort_menu.pack(side="left", padx=5)

tk.Button(top, text="Sort", command=filter_data).pack(side="left")

# Table
cols = ("ID","Title","Alt Titles","Rhythm","Meter","Key","Tempo","Source")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=100)
tree.pack(fill="both", expand=True)

# Details
details = tk.Text(root, wrap="word", height=10)
details.pack(fill="both", expand=True)

def show_details(_):
    sel = tree.selection()
    if sel:
        tune_id = tree.item(sel[0])["values"][0]
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
                "",
                f"Notation:\n{tune[8]}"
            ]))

tree.bind("<<TreeviewSelect>>", show_details)

# Initial load
load_data()

root.mainloop()
conn.close()