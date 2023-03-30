import sqlite3
import hashlib
import uuid

# Create a connection to the SQLite database
conn = sqlite3.connect('users.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create the users table if it doesn't already exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password_hash TEXT, salt TEXT)''')

def create_user(username, password):
    # Generate a random salt
    salt = uuid.uuid4().hex

    # Hash the password with the salt using SHA-256
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    # Insert the user into the database
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password_hash, salt))
    conn.commit()

def check_password(username, password):
    # Get the user's salt and password hash from the database
    c.execute("SELECT salt, password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()

    if result is not None:
        salt = result[0]
        password_hash = result[1]

        # Hash the password with the salt using SHA-256
        test_password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        # Compare the hash with the one in the database
        if test_password_hash == password_hash:
            return True

    return False

# Example usage
create_user('hacker', 'password123')
create_user('admin', 'password456')

print(check_password('hacker', 'password123')) # True
print(check_password('admin', 'wrongpassword')) # False