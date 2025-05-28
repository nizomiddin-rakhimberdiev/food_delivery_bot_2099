import sqlite3
import datetime

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("delivery.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id VARCHAR(20) NOT NULL UNIQUE,
                phone VARCHAR(20) NOT NULL,
                role VARCHAR(50) DEFAULT "user"
            );
            ''')
        self.cursor.execute('''
                            
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE                         
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE,
                description TEXT,
                price INTEGER,
                status INTEGER DEFAULT 1,
                image TEXT,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)                 
            );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(20),
            product_id INTEGER,
            count INTEGER DEFAULT 1,
            total_price INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(20),
            products TEXT,
            total_price INTEGER,
            status TEXT DEFAULT 'pending',
            address TEXT,
            old_phone VARCHAR(20),
            new_phone VARCHAR(20),
            created_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        ''')
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS adverts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id VARCHAR(20) NOT NULL UNIQUE,
                image TEXT NOT NULL,
                caption TEXT NOT NULL
            );
        """)

        self.connection.commit()
    def add_user (self, user_id, phone):
        try:
            self.cursor.execute('''INSERT INTO users (user_id, phone) VALUES (?, ?);''',
            (user_id, phone))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"User {user_id} already exists in the database.")
    def check_user(self, user_id):
        self.cursor.execute('''SELECT * FROM users WHERE user_id = ?;''', (user_id,))
        return self.cursor.fetchone() is not None
    
    def change_role(self, role, phone):
        self.cursor.execute("UPDATE users SET role=? WHERE phone=?", (role, phone))
        self.connection.commit()

    def check_admin(self, user_id):
        self.cursor.execute('''SELECT * FROM users WHERE user_id = ? AND role = "admin";''', (user_id,))
        return self.cursor.fetchone() is not None

    def add_category(self, name):
        try:
            self.cursor.execute('''INSERT INTO categories (name) VALUES (?);''', (name,))
            self.connection.commit()
            return "Category added successfully."
        except sqlite3.IntegrityError:
            return f"Category {name} already exists in the database."

    def get_categories(self):
        self.cursor.execute('''SELECT * FROM categories;''')
        return self.cursor.fetchall()

    def add_product(self, name, description, price, image, category_id):
        self.cursor.execute("""
        INSERT INTO products (name, description, price, image, category_id)
        VALUES (?, ?, ?, ?, ?)""", (name, description, price, image, category_id))
        self.connection.commit()

    def get_products(self, category_id):
        self.cursor.execute('''SELECT * FROM products WHERE category_id = ?;''', (category_id,))
        return self.cursor.fetchall()


    def get_product(self, product_id):
        self.cursor.execute('''SELECT * FROM products WHERE id = ?;''', (product_id,))
        return self.cursor.fetchone()
    
    def add_to_cart(self, product_id, user_id, count, price):
        total_price = int(count) * int(price)
        self.cursor.execute('''INSERT INTO cart (product_id, user_id, count, total_price) VALUES (?, ?, ?, ?);''', (product_id, user_id, count, total_price))
        self.connection.commit()
        
    def get_cart_data(self, user_id):
        self.cursor.execute('''SELECT * FROM cart WHERE user_id = ?;''', (user_id,))
        return self.cursor.fetchall()

    def create_order(self, user_id, address, phone):
        cart_data = self.get_cart_data(user_id)
        products = ""
        total_price = 0
        for cart in cart_data:
            product_id = cart[2]
            count = cart[3]
            total_price += cart[4]
            self.cursor.execute('''SELECT * FROM products WHERE id = ?;''', (product_id,))
            product = self.cursor.fetchone()
            products += f"{product[1]} - {count} x : {cart[4]} so'm\n"

        user = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        old_phone = user[2]
        new_phone = phone
        created_at = datetime.datetime.now()
        total_price += 15000
        self.cursor.execute('''INSERT INTO orders (user_id, products, total_price, address, old_phone, new_phone, created_at) VALUES (?, ?, ?, ?, ?, ?, ?);''', (user_id, products, total_price, address, old_phone, new_phone, created_at))
        self.connection.commit()

    def clear_cart(self, user_id):
        self.cursor.execute('''DELETE FROM cart WHERE user_id = ?;''', (user_id,))
        self.connection.commit()

    def get_all_users_user_id(self):
        data = self.cursor.execute('''SELECT user_id FROM users;''').fetchall()
        user_ids = [row[0] for row in data]
        return user_ids

    def delete_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS orders;''')
        self.connection.commit()

    def add_advert(self, message_id, image, caption):
        try:
            self.cursor.execute('''INSERT INTO adverts (message_id, image, caption) VALUES (?, ?, ?);''', (message_id, image, caption))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Advert with message_id {message_id} already exists in the database.")

    def get_advert(self, message_id):
        self.cursor.execute('''SELECT * FROM adverts WHERE message_id = ?;''', (message_id,))
        return self.cursor.fetchone()

db = Database()
# db.delete_table()
print(db.get_all_users_user_id())