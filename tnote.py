import argparse
import sqlite3
from rich.console import Console

console = Console()


def create_table():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  note TEXT NOT NULL);''')
    conn.commit()
    conn.close()


def add_note(title, note):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, note) VALUES (?, ?)", (title, note))
    conn.commit()
    conn.close()


def delete_note(id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()


def list_notes(search=None):
    conn = sqlite3.connect('notes.db')
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


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Note taking app.')

    parser.add_argument('-a', '--add', nargs=2, metavar=('title', 'note'), help='Add a new note.')

    parser.add_argument('-d', '--delete', type=int, metavar='id', help='Delete a note by id.')

    parser.add_argument('-l', '--list', action='store_true', help='List all notes.')

    parser.add_argument('-s', '--search', metavar='string', help='Search for any match string in title and note.')

    args = parser.parse_args()

    create_table()

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
