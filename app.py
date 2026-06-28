"""
File: app.py
Description: 一個簡單的 Flask 網頁。訪問 "/" 顯示 "我是功能一"；訪問 "/user" 連線至 MySQL 資料庫，提供用戶資料的查詢、新增與刪除功能。
"""
import os
import pymysql
from flask import Flask, request, redirect

app = Flask(__name__)

def get_db_connection():
    host = os.environ.get("DB_HOST", "localhost")
    port = int(os.environ.get("DB_PORT", 8625))
    
    conn = pymysql.connect(
        host=host,
        port=port,
        user="root",
        password="rootpassword",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS demo_db")
        cursor.execute("USE demo_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL
            )
        """)
    conn.select_db("demo_db")
    return conn

@app.route("/")
def index():
    return "我是功能一"

@app.route("/user")
def user_manager():
    try:
        conn = get_db_connection()
    except Exception as e:
        return f"資料庫連線失敗，請稍後重試。錯誤訊息: {e}", 500
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    conn.close()
    
    user_rows = "".join([
        f"<li>{u['name']} ({u['age']} 歲) <a href='/delete/{u['id']}'>[刪除]</a></li>"
        for u in users
    ])
    
    html = f"""
    <h1>用戶資料管理</h1>
    <form action="/add" method="POST">
        姓名: <input type="text" name="name" required>
        年紀: <input type="number" name="age" required>
        <button type="submit">新增</button>
    </form>
    <h2>用戶列表</h2>
    <ul>
        {user_rows if user_rows else "<li>目前無資料</li>"}
    </ul>
    """
    return html

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form.get("name")
    age = request.form.get("age")
    if name and age:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
                conn.commit()
            conn.close()
        except Exception as e:
            return f"新增失敗: {e}", 500
    return redirect("/user")

@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
        conn.close()
    except Exception as e:
        return f"刪除失敗: {e}", 500
    return redirect("/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
