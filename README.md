# codeguard-test
# User Authentication Module
import sqlite3

def login(username, password):
    API_KEY = "sk-prod-9xKpL2mNqR8vT4wY"  # hardcoded secret
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    return cursor.fetchone()

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    print(f"[LOG] Fetching PII data for user: {user_id}")
    return cursor.fetchall()
