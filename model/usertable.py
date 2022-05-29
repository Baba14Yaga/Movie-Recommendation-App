# DB Management
import sqlite3

def add_userdata(username,password):
    conn = sqlite3.connect('model/data.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS userstable
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    is_admin INTEGER DEFAULT 0,
                    password TEXT NOT NULL)''')
    try:
        cur.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    except:
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True
    
def login_user(username,password):
    conn = sqlite3.connect('model/data.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS userstable
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    is_admin INTEGER DEFAULT 0,
                    password TEXT NOT NULL)''')
    try:
        cur.execute('SELECT user_id FROM userstable WHERE username =? AND password = ?',(username,password))
        data = cur.fetchall()
    except:
        conn.close()
        return False
    if(len(data)==0):
        return False    
    conn.close()
    return  data[0][0]


