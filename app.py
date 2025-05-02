import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from sql_scripts import get_all_articles, get_article_by_id, get_all_reviews, add_review, add_article_to_db, increment_likes, has_liked, save_like

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

reviews_list = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    articles = get_all_articles()
    return render_template("index.html", articles=articles)

@app.context_processor
def inject_request():
    return dict(request=request)

@app.route("/search_suggestions")
def search_suggestions():
    query = request.args.get('query', '').lower()
    matches = [a for a in get_all_articles() if query in a[1].lower()]
    return jsonify(matches[:5])

@app.route("/search")
def search():
    query = request.args.get('query', '').lower()
    results = [a for a in get_all_articles() if query in a[1].lower()]
    return render_template("search_results.html", articles=results, query=query)

@app.route("/article/<int:article_id>")
def article_page(article_id):
    article = get_article_by_id(article_id)
    if article:
        return render_template("article_page.html", article=article)
    return "<h1>Стаття не знайдена</h1>"

@app.route("/add", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        image_path = request.form.get('image', '')

        image_file = request.files.get('image_file')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"img/{filename}"

        add_article_to_db(title, description, author, image_path)
        return redirect("/")

    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("add_article.html", images=image_files)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contacts")
def contacts_page():
    return render_template("contacts.html")

@app.route("/faq")
def faq_page():
    return render_template("faq.html")

@app.route("/resources")
def resources_page():
    return render_template("resources.html")

@app.route("/reviews", methods=["GET", "POST"])
def reviews_page():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")
        if username and message:
            add_review(username, message)
    all_reviews = get_all_reviews()
    return render_template("reviews.html", reviews=all_reviews)

@app.route("/like/<int:article_id>", methods=["POST"])
def like_article(article_id):
    ip = request.remote_addr
    if not has_liked(article_id, ip):
        save_like(article_id, ip)
    return redirect(url_for('article_page', article_id=article_id))

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
