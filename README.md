# tnote
The simple terminal note with sqlite to store data build by python script.

# Add profile PATH for global use command

`mv tnote.py tnote`

Make file can execute by user.

`chmod u+x tnote`

```zsh
# Setting PATH for Python 3.11
# The original version is saved in .zprofile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}:/Users/xxxxxx/Documents/GitHub/tnote"
export PATH
```

replace `/Users/xxxxxx/Documents/GitHub/tnote` with your tnote path

# How to use

```zsh
tnote -h
usage: tnote [-h] [-a title note] [-d id] [-l] [-s string]

Note taking app.

options:
  -h, --help            show this help message and exit
  -a title note, --add title note
                        Add a new note.
  -d id, --delete id    Delete a note by id.
  -l, --list            List all notes.
  -s string, --search string
                        Search for any match string in title and note.
```
