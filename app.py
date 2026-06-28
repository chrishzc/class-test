"""
File: app.py
Description: 一個簡單的 Flask 網頁應用程式，當訪問首頁時會顯示 "我是功能一"，並在 5000 port 運行。
"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "我是功能一"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
