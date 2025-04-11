from flask import Flask, render_template
from sql_scripts import get_all_articles, get_article_by_id

app = Flask(__name__)

@app.route("/")
def index():
    articles = get_all_articles()
    return render_template("index.html", articles=articles)

@app.route("/article/<int:article_id>")
def article_page(article_id):
    article = get_article_by_id(article_id)
    if article:
        return render_template("article_page.html", article=article)
    return "<h1>Стаття не знайдена</h1>"

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
