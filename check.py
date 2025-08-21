import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="tgroll",
        user="postgres",
        password="postgres1234"
    )
    print("Подключение успешно!")
    conn.close()
except Exception as e:
    print(f"Ошибка: {e}")