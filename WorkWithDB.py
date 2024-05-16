import sqlite3 as sq
from web3 import Web3

def create_table():
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS keys
        (
            key TEXT,
            address TEXT
        )
        """)
def add_new_key(new_key: str):
    w3 = Web3(Web3.HTTPProvider("https://arbitrum.drpc.org"))
    account = w3.eth.account.from_key(new_key)
    with sq.connect("data.db") as con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO keys (key, address) VALUES (?, ?)", (new_key, account.address))
            con.commit()
            print("Key and address added successfully.")
        except sq.Error as e:
            print(f"Error adding key and address: {e}")
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

def get_address_on_key(new_key: str):
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT address FROM keys WHERE key = ?", (new_key,))
        address = cur.fetchone()  # Используем fetchone() для получения одной строки
        return address[0] if address else None
def get_key_on_address(new_address: str):
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT key FROM keys WHERE address = ?", (new_address,))
        key = cur.fetchone()  # Используем fetchone() для получения одной строки
        return key[0] if key else None  # Возвращаем ключ или None, если ничего не найдено

def transfer_in_array_address():
    with sq.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT address FROM keys""")
        addresses = cur.fetchall()  # Получаем все строки результата

        return [address[0] for address in addresses]  # Преобразуем кортежи в список строк
