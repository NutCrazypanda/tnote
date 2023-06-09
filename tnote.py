#!/usr/local/bin/python3
import argparse
import sqlite3
from rich.console import Console
import os

console = Console()
dbfile  = '/xxxx/notes.db' #your db file

def create_table():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  note TEXT NOT NULL);''')
    conn.commit()
    conn.close()

def reset_primary_key():
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM notes")
    result = cursor.fetchone()[0]
    if result == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='notes'")
        #cursor.execute("INSERT INTO table_name (id, column1, column2) VALUES (1, 'value1', 'value2')")
        conn.commit()
    conn.close()

def add_note(title, note):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, note) VALUES (?, ?)", (title, note))
    conn.commit()
    conn.close()


def delete_note(id):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()


def list_notes(search=None):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()

    if search:
        c.execute("SELECT * FROM notes WHERE title LIKE ? OR note LIKE ?", ('%' + search + '%', '%' + search + '%'))
        rows = c.fetchall()

        if len(rows) == 0:
            console.print("No notes found.", style="bold red")
            return

        for row in rows:
            console.print(f"{row[0]}. [bold blue]{row[1]}[/bold blue] - {row[2]}", style="bold green")

        return

    else:
        c.execute("SELECT * FROM notes")
        rows = c.fetchall()

        if len(rows) == 0:
            console.print("No notes found.", style="bold red")
            return

        for row in rows:
            console.print(f"{row[0]}. [bold blue]{row[1]}[/bold blue] - {row[2]}", style="bold green")

# dump all notes and clear database and reinsert all notes
def reindex():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    rows = c.fetchall()
    conn.commit()

    # delete dbfile and create new one
    conn.close()
    os.remove(dbfile)
    create_table()

    for row in rows:
        add_note(row[1], row[2])


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Note taking app.')

    parser.add_argument('-a', '--add', nargs=2, metavar=('title', 'note'), help='Add a new note.')

    parser.add_argument('-d', '--delete', type=int, metavar='id', help='Delete a note by id.')

    parser.add_argument('-l', '--list', action='store_true', help='List all notes.')

    parser.add_argument('-s', '--search', metavar='string', help='Search for any match string in title and note.')

    parser.add_argument('-re', '--reindex', action='store_true', help='Reindex all notes.')
    args = parser.parse_args()

    create_table()
    try:
        reset_primary_key()
    except:
        None

    if args.add:
        add_note(args.add[0], args.add[1])
        console.print("Note added successfully.", style="bold green")

    elif args.delete:
        delete_note(args.delete)
        console.print("Note deleted successfully.", style="bold green")

    elif args.list:
        list_notes(args.search)

    elif args.search:
        list_notes(args.search)
    
    elif args.reindex:
        reindex()
        console.print("Reindex completed.", style="bold green")
