from flask import Flask, jsonify
from flask_cors import CORS  # Добавляем импорт
from models import create_tables
from handlers import AuthorHandlers, BookHandlers, UtilityHandlers

# Создаем Flask приложение
app = Flask(__name__)

# Включаем CORS для всех доменов (для разработки)
CORS(app)


# Альтернативно: более строгая настройка CORS
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Или настройка CORS вручную через заголовки
@app.after_request
def after_request(response):
    """Добавляем CORS заголовки к каждому ответу"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Обработка OPTIONS запросов для CORS
@app.route('/api/authors', methods=['OPTIONS'])
@app.route('/api/authors/<int:author_id>', methods=['OPTIONS'])
@app.route('/api/books', methods=['OPTIONS'])
@app.route('/api/books/<int:book_id>', methods=['OPTIONS'])
def options_handler():
    """Обработчик для OPTIONS запросов (CORS preflight)"""
    return '', 200


# ===== Роуты для Авторов =====
@app.route('/api/authors', methods=['GET'])
def get_authors():
    return AuthorHandlers.get_authors()


@app.route('/api/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    return AuthorHandlers.get_author(author_id)


@app.route('/api/authors', methods=['POST'])
def create_author():
    return AuthorHandlers.create_author()


@app.route('/api/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    return AuthorHandlers.update_author(author_id)


@app.route('/api/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    return AuthorHandlers.delete_author(author_id)


# ===== Роуты для Книг =====
@app.route('/api/books', methods=['GET'])
def get_books():
    return BookHandlers.get_books()


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    return BookHandlers.get_book(book_id)


@app.route('/api/books', methods=['POST'])
def create_book():
    return BookHandlers.create_book()


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    return BookHandlers.update_book(book_id)


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    return BookHandlers.delete_book(book_id)


# ===== Вспомогательные роуты =====
@app.route('/api/genres', methods=['GET'])
def get_genres():
    return UtilityHandlers.get_genres()


@app.route('/api/tags', methods=['GET'])
def get_tags():
    return UtilityHandlers.get_tags()


# Роут для проверки работы сервера
@app.route('/api/health', methods=['GET'])
def health_check():
    from datetime import datetime
    return jsonify({
        'status': 'OK',
        'message': 'Сервер работает нормально',
        'timestamp': datetime.now().isoformat()
    })


# Главная страница с документацией API
@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Books Library API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>Books Library API</h1>
            <p>Доступные endpoints:</p>

            <div class="endpoint">
                <strong>GET /api/health</strong> - Проверка работы сервера
            </div>

            <div class="endpoint">
                <strong>GET /api/authors</strong> - Список авторов<br>
                <strong>POST /api/authors</strong> - Создать автора<br>
                <strong>GET /api/authors/1</strong> - Получить автора<br>
                <strong>PUT /api/authors/1</strong> - Обновить автора<br>
                <strong>DELETE /api/authors/1</strong> - Удалить автора
            </div>

            <div class="endpoint">
                <strong>GET /api/books</strong> - Список книг<br>
                <strong>POST /api/books</strong> - Создать книгу<br>
                <strong>GET /api/books/1</strong> - Получить книгу<br>
                <strong>PUT /api/books/1</strong> - Обновить книгу<br>
                <strong>DELETE /api/books/1</strong> - Удалить книгу
            </div>

            <div class="endpoint">
                <strong>GET /api/genres</strong> - Список жанров<br>
                <strong>GET /api/tags</strong> - Список тегов
            </div>

            <p>Пример использования:</p>
            <pre>fetch('http://localhost:5000/api/authors')
    .then(response => response.json())
    .then(data => console.log(data));</pre>
        </body>
    </html>
    '''


# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Страница не найдена'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Внутренняя ошибка сервера'
    }), 500


# Запуск приложения
if __name__ == '__main__':
    # Создаем таблицы при первом запуске
    create_tables()

    print("=" * 60)
    print("Books Library API Server")
    print("=" * 60)
    print("Сервер запущен на http://localhost:5000")
    print("Главная страница: http://localhost:5000/")
    print("\nДоступные endpoints:")
    print("  GET    /api/health     - проверка работы сервера")
    print("  GET    /api/authors    - список авторов")
    print("  POST   /api/authors    - создать автора")
    print("  GET    /api/authors/1  - получить автора")
    print("  PUT    /api/authors/1  - обновить автора")
    print("  DELETE /api/authors/1  - удалить автора")
    print("  GET    /api/books      - список книг")
    print("  POST   /api/books      - создать книгу")
    print("  GET    /api/books/1    - получить книгу")
    print("  PUT    /api/books/1    - обновить книгу")
    print("  DELETE /api/books/1    - удалить книгу")
    print("  GET    /api/genres     - список жанров")
    print("  GET    /api/tags       - список тегов")
    print("=" * 60)

    # Запускаем сервер
    app.run(debug=True, host='0.0.0.0', port=5000)
