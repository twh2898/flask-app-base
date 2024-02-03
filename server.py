from flask import Flask, render_template

from app import init_app

app = Flask(__name__, static_folder='static',
            template_folder='templates')
app.secret_key = 'SECRET TUNNEL'
app.config['DATABASE'] = 'main.db'
init_app(app)


@app.route('/')
def index():
    return render_template('page/home.html')


@app.route('/instance')
def instance():
    return app.instance_path


@app.route('/create')
def create():
    return render_template('page/create.html')


@app.route('/review')
def review():
    return render_template('page/review.html')
