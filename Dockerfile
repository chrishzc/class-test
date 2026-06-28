# File: Dockerfile
# Description: 用於封裝 Flask 網頁應用程式的 Dockerfile，底層使用與專案一致的 Python 3.13 版本。

FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
