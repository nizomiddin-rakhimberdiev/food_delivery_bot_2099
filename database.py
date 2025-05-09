import sqlite3

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
    

