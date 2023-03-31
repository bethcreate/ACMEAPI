from random import Random
import sqlite3
from flask import Flask, jsonify, render_template, request, redirect
from models import Product

app = Flask(__name__)
db = "mydatabase.db"


def get_db_connection():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    products = Product.read_all(db)
    return jsonify(products)


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
