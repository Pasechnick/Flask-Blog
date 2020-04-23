from flask import Flask, render_template, url_for

app = Flask(__name__)


posts = [
    {
        'author': 'corey schafer',
        'title': 'blog post 1',
        'content': 'First post content',
        'date_posted': 'april 20, 2002'
    },

    {
        'author': 'alex mitu',
        'title': 'blog post 2',
        'content': 'second post content',
        'date_posted': 'april 23, 2012'
    }
]

@app.route("/")
@app.route("/home")
def home():
    # we got that posts value out home.html {% for post in posts %} so we can use them here by passing posts in our home fnc
    return render_template("home.html", posts = posts) 

@app.route("/about")
def about():
    return render_template("about.html", title="About")

if __name__ == '__main__':
    app.run(debug=True)




