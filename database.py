import threading, sqlite3

db = sqlite3.connect('baza.db', check_same_thread=False)
lock = threading.Lock()
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (id BIGINT, nick TEXT)""")
db.commit()

def get_allusers():
    text = '🗃 | Список всех пользователей:\n\n'
    idusernumber = 0
    for info in sql.execute(f"SELECT * FROM users"):
        idusernumber += 1
        text += f"{idusernumber}. {info[0]} ({info[1]})" + f" [{info[1]}](tg://user?id="+str(info[0])+")\n\n"
    return text

def add_user(user_name, user_id):
    sql.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES ({user_id}, '{user_name}')")
        db.commit()
    else:
        pass