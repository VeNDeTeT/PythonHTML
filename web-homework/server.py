#!/usr/bin/env python3
"""
Веб-сервер для домашки
Задание 2: На любой GET-запрос возвращает страницу "Контакты"
Но также может открывать разные страницы в зависимости от пути
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

# Путь к файлу контактов
CONTACTS_FILE = Path("contacts.html")


class RequestHandler(BaseHTTPRequestHandler):
    """Класс для обработки HTTP-запросов"""

    def do_GET(self):
        """Обработка GET-запроса"""
        print(f"\n[GET] Запрос к пути: {self.path}")

        # Извлекаем имя файла из пути
        # /index.html -> index.html
        # / -> contacts.html (по умолчанию)
        # /category.html -> category.html
        path = self.path.lstrip("/")

        if not path or path == "/":
            # На корневой путь / отдаём Контакты (как требует Задание 2)
            file_path = CONTACTS_FILE
        else:
            # Для других путей пытаемся открыть запрошенный файл
            file_path = Path(path)

        print(f"[GET] Ищем файл: {file_path}")

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
            print(f"[GET] ✓ Файл {file_path} отправлен")

        except FileNotFoundError:
            # Если файл не найден - отдаём Контакты (как требует Задание 2)
            print(f"[GET] ✗ Файл {file_path} не найден, отдаю Контакты")
            try:
                with open(CONTACTS_FILE, "rb") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(content))
                self.end_headers()
                self.wfile.write(content)
                print(f"[GET] ✓ Контакты отправлены")

            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h1>404 - Файл не найден</h1>".encode("utf-8"))
                print(f"[GET] ✗ Ошибка: contacts.html не найден")

    def do_POST(self):
        """Обработка POST-запроса"""
        print(f"\n[POST] Запрос получен")

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body_str = body.decode("utf-8", errors="replace")

        data = parse_qs(body_str)

        print("[POST] Полученные данные:")
        for key, values in data.items():
            for value in values:
                print(f"  {key} = {value}")

        response = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Спасибо</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-success">
                    <h4>Спасибо!</h4>
                    <p>Ваше сообщение успешно получено. Мы свяжемся с вами в скором времени.</p>
                </div>
            </div>
        </body>
        </html>
        """.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response)


# КОД ДЛЯ ЗАПУСКА СЕРВЕРА
if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    print("=" * 60)
    print("🚀 Сервер запущен на http://localhost:8000")
    print("=" * 60)
    print("Нажмите Ctrl+C для остановки\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n❌ Сервер остановлен")
