import sqlite3

print('USERS\n')
con = sqlite3.connect('sql.db')
cursor = con.cursor()
cursor.execute("SELECT * FROM users;")
print(cursor.fetchall())
print('\nOLDPOSTS\n')

con = sqlite3.connect('sql.db')
cursor = con.cursor()
cursor.execute("SELECT * FROM oldposts;")
print(cursor.fetchall())
print('\nLINKS\n')

con = sqlite3.connect('sql.db')
cursor = con.cursor()
cursor.execute("SELECT * FROM links;")
print(cursor.fetchall())