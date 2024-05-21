from flask import Flask, render_template, request, jsonify, url_for
import qrcode
from io import BytesIO
from base64 import b64encode
import json

app = Flask(__name__)

# Sample product data
products = {
    "1": {"name": "Milk", "description": "Fresh cow milk", "sizes": ["1 liter", "2 liters"], "colors": ["White"], "price": "$2.99", "availability": "In Stock"},
    "2": {"name": "Bread", "description": "Whole wheat bread", "sizes": ["Small", "Large"], "colors": ["Brown"], "price": "$1.49", "availability": "Only 10 packets left "}
}


@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<product_id>')
def product_page(product_id):
    if product_id not in products:
        return "Product not found", 404
    return render_template('product.html', product=products[product_id])

@app.route('/generate_qr/<product_id>')
def generate_qr(product_id):
    if product_id not in products:
        return "Product not found", 404

    product_url = url_for('product_page', product_id=product_id, _external=True)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(product_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = b64encode(buffer.getvalue()).decode()

    return jsonify({"qr_code": img_str, "product": products[product_id]})

if __name__ == '__main__':
    app.run(debug=True)
