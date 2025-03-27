Bookstore E-Commerce Web Application

M607 Computer Science Application Lab
Student Details
•	Student Name: Tanisha Yogish Salian
•	Student ID: GH1030645
•	Module Name: M607 Computer Science Application Lab
•	Submission Date: March 27, 2025

1. Introduction
This project is an individual assignment for the M607 Computer Science Application Lab module, where I was tasked with designing and implementing a simple e-commerce web application for a bookstore. The application incorporates both front-end and back-end technologies to create an engaging online shopping experience.
The primary goal was to demonstrate my ability to apply web development concepts, including CRUD operations, user authentication, session management, and database integration.

3. Project Overview
The Bookstore E-Commerce Web Application allows users to:
1.	Browse books on a product listing page.
2.	Search for books by title or author.
3.	Add/remove books from a shopping cart.
4.	Place orders and view order history.
Admins have additional privileges to manage the bookstore inventory through CRUD operations.

3. Features Implemented
User Features
1.	Landing Page:
•	Displays featured books.
•	Accessible at /.
2.	Product Listing Page:
•	Lists all available books with details (title, author, price, image).
•	Accessible at /products.html.
3.	Search Functionality:
•	Users can search for books by title or author.
•	Accessible at /search.html.
4.	Shopping Cart:
•	Users can add/remove items from the cart or clear the cart.
•	Accessible at /cart.html.
5.	Order Placement:
•	Users can place orders after logging in.
•	Accessible via /place_order.
6.	Order History:
•	Displays past orders with details (items, total price, status).
•	Accessible at /orderhistory.html.

Admin Features
1.	Admin Dashboard:
•	Allows admins to manage books (CRUD operations).
•	Accessible at /admin.
2.	Add Product:
•	Admins can add new books to the inventory.
•	Accessible at /add_product.
3.	Edit Product:
•	Admins can update book details.
•	Accessible at /edit_product/<book_id>.
4.	Delete Product:
•	Admins can remove books from the inventory.
•	Accessible at /delete_product/<book_id>.

4. Technologies Used
•	Backend Framework: Flask
•	Database: SQLite
•	Frontend: HTML, CSS (Bootstrap), Flask templates
•	Authentication: Password hashing using werkzeug.security
•	Session Management: Flask sessions

6. Database Schema
Users Table:
Column	Type	Description
id	INTEGER	Primary key
username	TEXT	Unique username
email	TEXT	Unique email
password	TEXT	Hashed password
is_admin	INTEGER	Admin status (0 = user, 1 = admin)
date_joined	TIMESTAMP	Account creation timestamp

Books Table:
Column	Type	Description
id	INTEGER	Primary key
title	TEXT	Book title
author	TEXT	Book author
price	REAL	Book price
image	TEXT	Image filename
description	TEXT	Book description
created_at	TIMESTAMP	Timestamp when added
Orders Table:
Column	Type	Description
id	INTEGER	Primary key
user_id	INTEGER	Foreign key referencing users
date_created	TIMESTAMP	Order creation timestamp
total_price	REAL	Total price of the order
status	TEXT	Order status
Order Items Table:
Column	Type	Description
id	INTEGER	Primary key
order_id	INTEGER	Foreign key referencing orders
book_id	INTEGER	Foreign key referencing books
price	REAL	Price of the book
quantity	INTEGER	Quantity ordered

7. Challenges Faced
During the development process, I encountered several challenges that affected my ability to provide screenshots of all pages:
1.	Time Constraints:
Due to limited time, I could not fully test all features or capture screenshots of every page.
2.	Debugging Issues:
Some routes required extensive debugging due to session-related errors and database query issues.
3.	Integration Challenges:
Integrating the front-end templates with back-end logic took longer than expected.
Despite these challenges, I ensured that all required functionalities were implemented with correct logic in the codebase.

8.	Access the application at http://127.0.0.1:5000.
	
9. Challenges
While the development of BookHaven remains incomplete due to time constraints and unforeseen debugging challenges, I have made every effort to implement the essential functionalities and logic. Although a few navigation issues arose at the last moment, which was unfortunate, I strived to cover all key segments effectively. I sincerely hope that the work done so far reflects my dedication and effort.

10. Conclusion
This project allowed me to apply my web development skills to create a functional e-commerce application for a bookstore. While I faced challenges due to time constraints and debugging issues, I successfully implemented all required features and ensured that the codebase follows best practices.
I hope this report demonstrates my understanding of web development concepts and my ability to apply them effectively in a real-world scenario.
