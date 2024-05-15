import sqlite3 as sq

def create_table():
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS keys
        (
            key TEXT
        )
        """)
def add_new_key(new_key: str):
    with sq.connect("data.db") as con:
        cur = con.cursor()
        print(new_key)
        cur.execute("INSERT INTO keys (key) VALUES (?)", (new_key,))
def delete_all(dell_key: str):
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("DELETE * FROM keys")
def dell_key(dell_key: str):
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM keys WHERE key = ?", (dell_key,))
def transfer_in_array():
    with sq.connect("data.db") as con:
        cur = con.cursor()

        cur.execute("""SELECT key FROM keys""")
        keys = cur.fetchall()  # Получаем все строки результата

        return [key[0] for key in keys]  # Преобразуем кортежи в список строк