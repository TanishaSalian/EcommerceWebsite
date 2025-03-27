import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    
    conn = sqlite3.connect("bookstore.db")
    conn.row_factory = sqlite3.Row
    
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL,
        image TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_price REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
  
    conn.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    )
    ''')
    
    

    admin_exists = conn.execute("SELECT id FROM users WHERE username = ?", ("admin",)).fetchone()
    if not admin_exists:
        conn.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ("admin", "tanisha@gmail.com", generate_password_hash("tanisha846", method='pbkdf2:sha256'), 1)
        )
    
    books = [
        {"id": 1, "title": "Fault in Our Stars", "author": "John Green", "price": 6.99, "image": "fault.jpg", 
         "description": "A heartbreaking story of two cancer riiden teenagers,Augustus waters and Hazel Lancaster"},
        {"id": 2, "title": "Jane Eyre", "author": "Charlotte Bronte", "price": 6.99, "image": "jane.jpg", 
         "description": "A tale of young wooman Jane and her love for Mr Rochester"},
        {"id": 3, "title": "The Alchemist", "author": "Paulo Coelho", "price": 5.99, "image": "download-1.jpg", 
         "description": "Paulo Coelho's first novel on manifestation, love and search for finding purpose."},
        {"id": 4, "title": "Read People Like Book", "author": "Thomas King", "price": 9.99, "image": "download-2.jpg", 
         "description": "A book to understand human behavior and body language."},
        {"id": 5, "title": "Pride and Prejudice", "author": "Jane Austen", "price": 7.49, "image": "pride.jpg", 
         "description": "one of Jane Austen' finest works, Pride and Prejudice follows the relationship between Elizabeth Bennet and her suitoor Mr Darcy, an aristocrat."},
        {"id": 6, "title": "Ikigai", "author": "Héctor García & Francesc Miralles", "price": 3.99, "image": "japenesebook.png", 
         "description": "Book is about Japanese way of living."},
        {"id": 7, "title": "Lord of the Flies", "author": "William Golding", "price": 12.99, "image": "download.jpg", 
         "description": "A survival storry about group of boys."},
        {"id": 8, "title": "Biography of Dr. A.P.J. Abdul Kalam", "author": "Arun Tiwari", "price": 5.99, "image": "dr_abdul.jpg", 
         "description": "A biography on A.P.J abdul Kalam,one of India's president known as the people's president."},
        {"id": 9, "title": "Dune", "author": "Frank Herbert", "price": 9.99, "image": "dune.jpg", 
         "description": "A scifi book about Paul Atredies."}
    ]
    
    for book in books:
        exists = conn.execute("SELECT id FROM books WHERE title = ? AND author = ?", (book["title"], book["author"])).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO books (title, author, price, image, description) VALUES (?, ?, ?, ?, ?)",
                (book["title"], book["author"], book["price"], book["image"], book["description"])
            )
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
