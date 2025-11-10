from flask import Flask, jsonify, request
from db_config import get_connection
from datetime import datetime

app = Flask(__name__)

# ---------- HOME ROUTE ----------
@app.route('/')
def home():
    print("✅ Home route accessed!")
    return jsonify({"message": "Welcome to E-Commerce Data Management API"})


# ---------- TEST DATABASE ----------
@app.route('/test_db')
def test_db():
    try:
        conn = get_connection()
        if conn:
            conn.close()
            return jsonify({"message": "✅ Database connection successful"})
        else:
            return jsonify({"error": "❌ Database connection failed"})
    except Exception as e:
        return jsonify({"error": str(e)})


# ---------- PRODUCTS ----------
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    stock = data.get('stock')

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)",
            (name, category, price, stock)
        )
        conn.commit()
        return jsonify({"message": "✅ Product added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur.close()
        conn.close()


@app.route('/get_products', methods=['GET'])
def get_products():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur.close()
        conn.close()


# ---------- SALES ----------
@app.route('/add_sale', methods=['POST'])
def add_sale():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))
        cur.execute("INSERT INTO sales (product_id, quantity, sale_date) VALUES (%s, %s, %s)",
                    (product_id, quantity, datetime.now()))
        conn.commit()
        return jsonify({"message": "✅ Sale recorded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur.close()
        conn.close()


@app.route('/get_sales_summary', methods=['GET'])
def get_sales_summary():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        query = """
        SELECT p.name AS product_name,
               SUM(s.quantity) AS total_sold,
               SUM(s.quantity * p.price) AS total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.name
        ORDER BY total_revenue DESC;
        """
        cur.execute(query)
        summary = cur.fetchall()
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur.close()
        conn.close()


# ---------- MAIN ENTRY ----------
if __name__ == '__main__':
    print("🚀 Flask app started...")
    app.run(debug=True)
