import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

# Default manager user
cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('mgr0', 'mgr0', 'manager')
            )

# Default doctor user
cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('doc0', 'doc0', 'doctor')
            )

# Default assistant user
cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('ast0', 'ast0', 'assistant')
            )

connection.commit()
connection.close()