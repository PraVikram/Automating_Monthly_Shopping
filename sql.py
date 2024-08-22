import sqlite3

conn = sqlite3.connect('grocery_items.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS groceries(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL)
               ''')

grocery_items = [('Milk',), ('Bread',)]
''', ('Bread',), ('Eggs',), ('Rice',), ('Sugar',)'''
cursor.executemany('INSERT INTO groceries (name) VALUES (?)', grocery_items)

conn.commit()
conn.close()