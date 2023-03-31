import sqlite3


class Product:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def create(self, db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO products (id, name, description, price) VALUES (?, ?, ?, ?)",
                  (self.id, self.name, self.description, self.price))
        conn.commit()
        conn.close()

    def read_all(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        products = c.execute('SELECT * FROM products').fetchall()
        return products

    def read_one(db, id):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        product = c.execute(
            'SELECT * FROM products WHERE id =?', (id,)).fetchone()
        return product

    def update_product(db, product):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('UPDATE products SET name =?, description =?, price =? WHERE id =?',
                  (product.name, product.description, product.price, product.id))
        conn.commit()
        conn.close()

    def delete(db, id):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('DELETE FROM products WHERE id =?', (id,))
        conn.commit()
        conn.close()
