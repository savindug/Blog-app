from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from feed import Feed
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

Posts = Feed()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/feed')
def feed():
    return render_template('feed.html', posts=Posts)


@app.route('/post/<string:id>/')
def getPost(id):
    #     for p in Posts:
    #         if p.id == id:
    #             print(p)
    return render_template('post.html', post=id)


class RegisterForm (Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.data_required(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confim Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
