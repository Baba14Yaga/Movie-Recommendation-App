import sqlite3  

def insert_rating(user_id,movie_id,rating):
    movie_id=int(movie_id)
    con=sqlite3.connect('model/data.db')
    cur=con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ratings 
                (user_id INTEGER ,
                movie_id INTEGER, 
                rating INTEGER, 
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, movie_id))''')
    cur.execute('INSERT OR REPLACE INTO ratings (user_id,movie_id,rating) VALUES ( ? , ? , ? )',(user_id,movie_id,rating)) 
    con.commit()
    con.close()
def fetch_rating(user_id,movie_id):
    movie_id=int(movie_id)
    rating=0
    con=sqlite3.connect('model/data.db')
    cursor=con.cursor()
    try:
        cursor.execute('SELECT rating FROM ratings WHERE user_id =? AND movie_id=? ', (user_id , movie_id))
        record = cursor.fetchone()
        if record!=None:
            rating= record[0]
        else:
            rating = 0   
    except sqlite3.Error as er:
        pass
    cursor.close()    
    con.close()
    return  rating    
    

def show_rating(user_id,movie_id,rating):

    con=sqlite3.connect('model/data.db')
    cur=con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ratings 
                (user_id INTEGER ,
                movie_id INTEGER, 
                rating INTEGER, 
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, movie_id))''')
    cur.execute('') 
    con.commit()
    con.close()
