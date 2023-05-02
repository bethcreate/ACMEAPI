from db import get_db

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

    











# class Product:
#     def __init__(self, id, name, description, price):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.price = price

#     def create(self, db):
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         c.execute("INSERT INTO products (id, name, description, price) VALUES (?, ?, ?, ?)",
#                   (self.id, self.name, self.description, self.price))
#         conn.commit()
#         conn.close()

#     def read_all(db):
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         products = c.execute('SELECT * FROM products').fetchall()
#         return products

#     def read_one(db, id):
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         product = c.execute(
#             'SELECT * FROM products WHERE id =?', (id,)).fetchone()
#         return product

#     def update_product(db, product):
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         c.execute('UPDATE products SET name =?, description =?, price =? WHERE id =?',
#                   (product.name, product.description, product.price, product.id))
#         conn.commit()
#         conn.close()

#     def delete(db, id):
#         conn = sqlite3.connect(db)
#         c = conn.cursor()
#         c.execute('DELETE FROM products WHERE id =?', (id,))
#         conn.commit()
#         conn.close()
