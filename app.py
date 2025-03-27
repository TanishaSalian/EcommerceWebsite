import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "supersecretkey" 


def get_db_connection():
    conn = sqlite3.connect("bookstore.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        if user:
            g.user = dict(user)

@app.route("/")
def index():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books LIMIT 6").fetchall()
    conn.close()
    return render_template("index.html", books=books)


@app.route("/products.html")
def products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("products.html", books=books)


@app.route('/search.html', methods=['GET'])
def search():
    query = request.args.get('query', '') 
    if not query:
        return render_template("search.html", books=[], query="")
    
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                         ('%' + query + '%', '%' + query + '%')).fetchall()
    conn.close()
    
    return render_template("search.html", books=books, query=query)


@app.route("/cart.html")
def cart():
    cart_items = session.get("cart", [])
    total_price = sum(float["price"] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)


@app.route("/add_to_cart/<int:book_id>")
def add_to_cart(book_id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    
    if not book:
        flash("Book not found", "error")
        return redirect(url_for('products'))
        book_dict = dict(book)
    

    if "cart" not in session:
        session["cart"] = []
    
   
    for item in session["cart"]:
        if item["id"] == book_dict["id"]:
            flash("Book already in cart", "info")
            return redirect(url_for('cart'))
    
    

@app.route("/remove_from_cart/<int:book_id>")
def remove_from_cart(book_id):
    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["id"] != book_id]
        session.modified = True
        flash("Item removed from cart", "success")
    
    return redirect(url_for('cart'))


@app.route("/clear_cart")
def clear_cart():
    session["cart"] = []
    session.modified = True
    flash("Cart cleared", "success")
    return redirect(url_for('cart'))


@app.route("/place_order", methods=["POST"])
def place_order():
    if "user_id" not in session:
        flash("Please login to place an order", "error")
        return redirect(url_for('login'))
    
    cart_items = session.get("cart", [])
    if not cart_items:
        flash("Your cart is empty", "error")
        return redirect(url_for('cart'))
    
    total_price = sum(float(item["price"]) for item in cart_items)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    
    cursor.execute(
        "INSERT INTO orders (user_id, total_price, status) VALUES (?, ?, ?)",
        (session["user_id"], total_price, "Pending")
    )
    
    order_id = cursor.lastrowid
    
    # Add order items
    for item in cart_items:
        cursor.execute(
            "INSERT INTO order_items (order_id, book_id, price, quantity) VALUES (?, ?, ?, ?)",
            (order_id, item["id"], item["price"], 1)
        )
    
    conn.commit()
    conn.close()
    
    
    session["cart"] = []
    session.modified = True
    
    flash("Order placed successfully!", "success")
    return redirect(url_for('order_history'))


@app.route("/orderhistory.html")
def order_history():
    if "user_id" not in session:
        flash("Please login to view order history", "error")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    orders = conn.execute("""
        SELECT o.id, o.date_created, o.total_price, o.status,
               COUNT(oi.id) as item_count
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        WHERE o.user_id = ?
        GROUP BY o.id
        ORDER BY o.date_created DESC
    """, (session["user_id"],)).fetchall()
    
    
    orders_with_items = []
    for order in orders:
        order_dict = dict(order)
        
        items = conn.execute("""
            SELECT oi.*, b.title, b.author, b.image
            FROM order_items oi
            JOIN books b ON oi.book_id = b.id
            WHERE oi.order_id = ?
        """, (order["id"],)).fetchall()
        
        order_dict["items"] = [dict(item) for item in items]
        orders_with_items.append(order_dict)
    
    conn.close()
    
    return render_template("orderhistory.html", orders=orders_with_items)


@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            flash("Logged in successfully", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "error")
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        
        conn = get_db_connection()
        existing_user = conn.execute("SELECT id FROM users WHERE username = ? OR email = ?", 
                                   (username, email)).fetchone()
        
        if existing_user:
            conn.close()
            flash("Username or email already exists", "error")
            return render_template("login.html", register=True)
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn.execute("INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
                   (username, email, hashed_password, 0))
        conn.commit()
        conn.close()
        
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    
    return render_template("login.html", register=True)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out", "success")
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    if not g.user or not g.user.get("is_admin"):
        flash("Access denied", "error")
        return redirect(url_for("index"))
    
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    
    return render_template("admin.html", books=books)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if not g.user or not g.user.get("is_admin"):
        flash("Access denied", "error")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]
        image = request.form["image"]
        description = request.form["description"]
        
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO books (title, author, price, image, description) 
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, price, image, description))
        conn.commit()
        conn.close()
        
        flash("Product added successfully", "success")
        return redirect(url_for("admin"))
    
    return render_template("add_product.html")


@app.route("/edit_product/<int:book_id>", methods=["GET", "POST"])
def edit_product(book_id):
    if not g.user or not g.user.get("is_admin"):
        flash("Access denied", "error")
        return redirect(url_for("index"))
    
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    
    if not book:
        conn.close()
        flash("Book not found", "error")
        return redirect(url_for("admin"))
    
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        price = request.form["price"]
        image = request.form["image"]
        description = request.form["description"]
        
        conn.execute("""
            UPDATE books 
            SET title = ?, author = ?, price = ?, image = ?, description = ? 
            WHERE id = ?
        """, (title, author, price, image, description, book_id))
        conn.commit()
        
        flash("Product updated successfully", "success")
        return redirect(url_for("admin"))
    
    conn.close()
    return render_template("edit_product.html", book=book)


@app.route("/delete_product/<int:book_id>")
def delete_product(book_id):
    if not g.user or not g.user.get("is_admin"):
        flash("Access denied", "error")
        return redirect(url_for("index"))
    
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    
    flash("Product deleted successfully", "success")
    return redirect(url_for("admin"))
