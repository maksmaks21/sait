import sqlite3

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
    cursor.execute('INSERT INTO reviews (author, text) VALUES (?, ?)', (author, text))
    conn.commit()
    conn.close()

# Отримати всі відгуки
def get_all_reviews():
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews ORDER BY created DESC')
    reviews = cursor.fetchall()
    conn.close()
    return reviews
