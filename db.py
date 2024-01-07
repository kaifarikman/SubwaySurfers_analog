import sqlite3


def get_connection():
    conn = sqlite3.connect('db.db')
    return conn


def start_session():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS information (
            nickname TEXT,
            music BOOLEAN,
            audios BOOLEAN,
            skin TEXT,
            wallpaper TEXT,
            record INTEGER)""")


def get_information_from_db():
    with get_connection() as conn:
        cur = conn.cursor()
        query = cur.execute("""SELECT * FROM information""")
        try:
            return query.fetchall()[0]
        except:
            return tuple()


def update_information(data: dict):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""DELETE FROM information""")
        data = tuple(data.values())
        cur.execute("""INSERT INTO information VALUES (?, ?, ?, ?, ?, ?)""", data)
        conn.commit()


def update_record(record: str):
    with get_connection() as conn:
        cur = conn.cursor()
        information = get_information_from_db()
        if information:
            rec = int(information[-1])
            info = information[:-1]
        else:
            info = tuple(('', True, True, 'skin2', 'wallpaper2'))
            rec = 0
        print(info, rec)
        if int(record) > rec:
            new_information = info + (record,)
            cur.execute("""DELETE FROM information""")
            cur.execute("""INSERT INTO information VALUES (?, ?, ?, ?, ?, ?)""", new_information)
            conn.commit()
