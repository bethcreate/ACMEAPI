from random import Random
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
from models import Product
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)
db = SQLAlchemy(app)
db.init_app(app)
bcrpt=Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'scretekey'

# db = "mydatabase.db"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True) 

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=20)],render_kw={"placeholder":"username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=20)],render_kw={"placeholder": "password"})
    
    submit = SubmitField("Register")

    def validate(self,username):
        existing_user_username= User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("The username already exists")
    

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder":"username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4,max=20)],render_kw={"placeholder": "password"})
    
    submit = SubmitField("login")
 

# Home page
@app.route('/')
def home():
    products = Product.read_all(db)
    return render_template('home.html',{products})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter.filter_by(username=form.username.data).first()
        if user:
            if bcrpt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/register' , methods=['GET', 'POST'])
def register():
    form = RegistrationForm

    if form.validate_on_submit():
        hashed_password = bcrpt.generate_password_hash(form.password.data)
        new_user = User(username= form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('Login'))

    return render_template('register.html', form=form)

    # if 'username' in session:
    #     return render_template('home.html', username=session['username'])
    # else:
    #     return redirect('/login')




def get_db_connection():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        id = Random().randint(0, 10000)
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        product = Product(id, name, description, price)
        product.create(db)
        return redirect("/")
    else:
        return jsonify({"error": "This is a post request"})


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    product = conn.execute(
        'SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        conn.execute('UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?',
                     (name, description, price, id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template('edit.html', product=product)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)