FROM python:3.11-slim

WORKDIR /app

# 1) зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) исходники
COPY . .

# 3) запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]