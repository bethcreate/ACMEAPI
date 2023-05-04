from flask import Flask, jsonify, request
from flask_appbuilder import models
from db import create_tables


app = Flask(__name__)

@app.route('/products', methods=["GET"])
def read_all_products():
    products = models.read_all_products()
    return jsonify(products)

@app.route("/product",methods=["POST"])
def insert_product():
    product_details = request.get_json()
    name = product_details["name"]
    description = product_details["description"]
    price = product_details["price"]
    result = models.insert_product(name, description, price)
    return jsonify(result)

@app.route("/product", methods=["PUT"])
def update_product():
    product_details = request.get_json()
    id = product_details["id"]
    name = product_details["name"]
    description = product_details["description"]
    price = product_details["price"]
    result = models.update_product(id, name, description, price)
    return jsonify(result)

@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    result = models.delete_product(id)
    return jsonify(result)

@app.route("/product/<id>", methods=["GET"])
def read_one_product(id):
    product = models.get_by_id(id)
    return jsonify(product)

if __name__=="__app__":
    create_tables()

    app.run(host='0.0.0.0', port=8000, debug=False)
   