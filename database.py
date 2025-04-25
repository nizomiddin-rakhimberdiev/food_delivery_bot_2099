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

