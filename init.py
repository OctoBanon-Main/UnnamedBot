import sqlite3

def startup():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS report_channel (channel_id INTEGER, guild_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS warns (user_id INTEGER, guild_id INTEGER, warns INTEGER)")