from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Andy'}
    return render_template('index.html', title="Warm Welcome", user=user)