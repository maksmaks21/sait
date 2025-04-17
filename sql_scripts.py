import sqlite3

def get_all_articles():
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_article_by_id(article_id):
    conn = sqlite3.connect('ddd.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE id=?', (article_id,))
    article = cursor.fetchone()
    conn.close()
    return article


