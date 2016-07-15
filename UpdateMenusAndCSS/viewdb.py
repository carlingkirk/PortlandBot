import sqlite3

con = sqlite3.connect('sql.db')
cursor = con.cursor()

#con.execute('DROP TABLE IF EXISTS users')
#con.execute('DROP TABLE IF EXISTS oldposts')
#con.execute('DROP TABLE IF EXISTS links')
#con.commit()

#con.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, lastpost TEXT)')
#print('Loaded Users')
#con.execute('CREATE TABLE IF NOT EXISTS oldposts(stamp TEXT, id TEXT)')
#print('Loaded Oldposts')
#con.execute('CREATE TABLE IF NOT EXISTS links(title TEXT, url TEXT)')
#print('Loaded Links')
#con.commit()

domain = 'Portland'

cursor.execute("DELETE FROM links WHERE title LIKE 'classifieds'")
cursor.execute("DELETE FROM links WHERE title LIKE 'events'")
cursor.execute("DELETE FROM links WHERE title LIKE 'rant'")
#cursor.execute("DELETE FROM links WHERE title LIKE 'rave'")
#cursor.execute("INSERT INTO oldposts VALUES( '48w4ah' )")
#cursor.execute("DELETE FROM oldposts WHERE id LIKE '494qyg'")
#cursor.execute("UPDATE links SET id = '4ido6z' WHERE title LIKE 'classifieds'")
#cursor.execute("UPDATE links SET id = '4ido5l' WHERE title LIKE 'events'")

cursor.execute("INSERT INTO links VALUES( 'classifieds', '" + domain + "/comments/4ljja0' )")
cursor.execute("INSERT INTO links VALUES( 'events', '" + domain + "/comments/4ljj8q' )")
#cursor.execute("INSERT INTO links VALUES( 'hiring', '" + domain + "/comments/4h854e' )")
#cursor.execute("INSERT INTO links VALUES( 'hireme', '" + domain + "/comments/4h854j' )")
cursor.execute("INSERT INTO links VALUES( 'rant', '" + domain + "/comments/4lpnq3' )")
#cursor.execute("INSERT INTO links VALUES( 'rave', '" + domain + "/comments/4i582k' )")

#con.commit()


print('USERS\n')
cursor.execute("SELECT * FROM users;")
print(cursor.fetchall())

print('\nOLDPOSTS\n')
cursor.execute("SELECT * FROM oldposts;")
print(cursor.fetchall())

print('\nLINKS\n')
cursor.execute("SELECT * FROM links;")
print(cursor.fetchall())