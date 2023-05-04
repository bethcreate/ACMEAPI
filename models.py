from db import get_db
from flask_appbuilder import Model

def insert_product(name, description, price):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO products(name,description, price) VALUES (?,?,?)"
    cursor.execute(statement, [name, description, price])
    db.commit()
    return True

def update_product(id,name, description, price):
    db = get_db()
    cursor = db.cursor()
    statement ="UPDATE products SET name = ?, description = ?, price = ? WHERE id= ?"
    cursor.execute(statement, [name, description, price, id])
    db.commit()
    return True

def delete_product(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM products WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True

def read_one_product(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, description, price FROM products WHERE id = ?"
    cursor.execute(statement,[id])
    return cursor.fetchone()


def read_all_products():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, name, description, price FROM products"
    cursor.execute(query)
    return cursor.fetchall()

