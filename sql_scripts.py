import sqlite3
from datetime import datetime

# Отримання всіх статей
def get_all_articles():
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()
    return articles

# Отримання статті по ID
def get_article_by_id(article_id):
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE id=?', (article_id,))
    article = cursor.fetchone()
    conn.close()
    return article

# Додавання нової статті в базу
def add_article_to_db(title, text, author, image):
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (title, text, author, image)
        VALUES (?, ?, ?, ?)
    ''', (title, text, author, image))
    conn.commit()
    conn.close()

# Додати відгук
def add_review(author, text):
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    created = datetime.now().strftime("%d.%m.%Y.%H.%M")#Автоматичний час
    cursor.execute('INSERT INTO reviews (author, text, created) VALUES (?, ?, ?)', (author, text, created))
    conn.commit()
    conn.close()

# Отримати всі відгуки
def get_all_reviews():
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('SELECT author, text, created FROM reviews ORDER BY created DESC')
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def increment_likes(article_id):
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE articles SET likes = likes + 1 WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()

def has_liked(article_id, ip):
    conn = sqlite3.connect("ddd.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM likes_log WHERE article_id=? AND ip=?", (article_id, ip))
    result= cursor.fetchone()
    conn.close()
    return result is not None

def save_like(article_id, ip):
    conn = sqlite3.connect("ddd.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO likes_log (article_id, ip) VALUES (?, ?)", (article_id, ip))
        cursor.execute("UPDATE articles SET likes = likes + 1 WHERE id = ?", (article_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass #Вже лайкав
    conn.close()