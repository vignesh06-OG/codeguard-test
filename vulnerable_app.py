import sqlite3
import os

# User Authentication Module
def login(username, password):
    API_KEY = "sk-prod-9xKpL2mNqR8vT4wY"  # hardcoded secret
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    return cursor.fetchone()

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    print(f"[LOG] Fetching PII data for user: {user_id}")
    return cursor.fetchall()

def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id={user_id}")
    conn.commit()
