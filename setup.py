from sqlite3 import connect


db = connect("bot.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS end_text (text, status)")
cur.execute("INSERT INTO end_text VALUES ('تست', 'off')")
db.commit()
# cur.execute("CREATE TABLE IF NOT EXISTS text_status")