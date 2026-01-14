import sqlite3

conn = sqlite3.connect("blog_zsoptij.db")
tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

print(tables)

tables = conn.execute(
    "SELECT * FROM user;"
).fetchall()

print (tables)

tables = conn.execute(
    "SELECT * FROM tag;"
).fetchall()

print (tables)

tables = conn.execute(
    "SELECT * FROM post;"
).fetchall()

print (tables)

tables = conn.execute(
    "SELECT * FROM posttag;"
).fetchall()

print (tables)
