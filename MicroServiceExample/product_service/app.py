from flask import Flask, request, jsonify, abort

app = Flask(__name__)

products = [
    {"id": 1, "name": "Nike Sweatshirt", "price": 19.99},
    {"id": 2, "name": "Flip Flops", "price": 29.99}
]

@app.route('/products', methods=['POST'])
def create_product():
    if not request.json or 'name' not in request.json or 'price' not in request.json:
        abort(400, description="Please provide product name and price.")
    
    new_product = {
        'id': products[-1]['id'] + 1 if products else 1, 
        'name': request.json['name'],
        'price': request.json['price']
    }
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if not product:
        abort(404, description="Product not found.")
    if not request.json:
        abort(400, description="Request must be JSON.")
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400, description="Name must be a string.")
    if 'price' in request.json and type(request.json['price']) not in [int, float]:
        abort(400, description="Price must be a number.")

    product['name'] = request.json.get('name', product['name'])
    product['price'] = request.json.get('price', product['price'])
    return jsonify(product)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [prod for prod in products if prod['id'] != product_id]
    return jsonify({'result': True})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product is not None:
        return jsonify(product)
    else:
        abort(404, description="Product not found.")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "PRODUCTS UP"}), 200

if __name__ == '__main__':
    app.run(port=5001)
