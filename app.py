import os

from flask import Flask, render_template, redirect, request, flash, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


migrate = Migrate(app, db)


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", employees=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    errors = []
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            data = Data(name, email, phone)
            db.session.add(data)
            db.session.commit()
            flash("Employee Inserted Successfully")
        except:
            errors.append("Unable to add item to database.")
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    errors = []
    if request.method == 'POST':
        try:
            data = Data.query.get(request.form.get('id'))
            data.name = request.form['name']
            data.email = request.form['email']
            data.phone = request.form['phone']

            db.session.commit()
            flash("Employee Updated Successfully")
        except:
            errors.append("Unable to update item to database.")
    return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    errors = []
    try:
        data = Data.query.get(id)
        db.session.delete(data)
        db.session.commit()
        flash("Employee Deleted Successfully")
    except:
        errors.append("Unable to delete item from database.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
