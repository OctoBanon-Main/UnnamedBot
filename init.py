import sqlite3

def startup():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS guild_warnings (member_id INTEGER, guild_id INTEGER, warnings INTEGER)")