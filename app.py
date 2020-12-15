from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from feed import Feed
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MYSQL

mysql = MySQL(app);

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
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You have Successfully Registered to the Flask Blog', 'success')

        redirect(url_for('index'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key = '123'
    app.run(debug=True)
