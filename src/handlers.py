from flask import jsonify, request
from src.database import DatabaseManager


class AuthorHandlers:
    """Обработчики запросов для авторов"""

    @staticmethod
    def get_authors():
        """GET /api/authors - Получить всех авторов"""
        try:
            authors = DatabaseManager.get_all_authors()
            return jsonify({
                'success': True,
                'data': authors,
                'count': len(authors)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def get_author(author_id):
        """GET /api/authors/<id> - Получить автора по ID"""
        try:
            author = DatabaseManager.get_author_by_id(author_id)
            if author:
                return jsonify({
                    'success': True,
                    'data': author
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Автор не найден'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def create_author():
        """POST /api/authors - Создать нового автора"""
        try:
            # Получаем данные из тела запроса
            data = request.get_json()

            # Проверяем обязательные поля
            if not data or 'name' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Обязательное поле "name" отсутствует'
                }), 400

            # Создаем автора
            author, error = DatabaseManager.create_author(data)

            if author:
                return jsonify({
                    'success': True,
                    'data': author,
                    'message': 'Автор успешно создан'
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': error
                }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def update_author(author_id):
        """PUT /api/authors/<id> - Обновить автора"""
        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'Данные для обновления отсутствуют'
                }), 400

            author, error = DatabaseManager.update_author(author_id, data)

            if author:
                return jsonify({
                    'success': True,
                    'data': author,
                    'message': 'Автор успешно обновлен'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': error
                }), 404 if error == "Автор не найден" else 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def delete_author(author_id):
        """DELETE /api/authors/<id> - Удалить автора"""
        try:
            success, error = DatabaseManager.delete_author(author_id)

            if success:
                return jsonify({
                    'success': True,
                    'message': 'Автор успешно удален'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': error
                }), 404 if error == "Автор не найден" else 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500


class BookHandlers:
    """Обработчики запросов для книг"""

    @staticmethod
    def get_books():
        """GET /api/books - Получить все книги"""
        try:
            books = DatabaseManager.get_all_books()
            return jsonify({
                'success': True,
                'data': books,
                'count': len(books)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def get_book(book_id):
        """GET /api/books/<id> - Получить книгу по ID"""
        try:
            book = DatabaseManager.get_book_by_id(book_id)
            if book:
                return jsonify({
                    'success': True,
                    'data': book
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Книга не найдена'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def create_book():
        """POST /api/books - Создать новую книгу"""
        try:
            data = request.get_json()

            # Проверяем обязательные поля
            if not data or 'title' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Обязательное поле "title" отсутствует'
                }), 400

            book, error = DatabaseManager.create_book(data)

            if book:
                return jsonify({
                    'success': True,
                    'data': book,
                    'message': 'Книга успешно создана'
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': error
                }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def update_book(book_id):
        """PUT /api/books/<id> - Обновить книгу"""
        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'Данные для обновления отсутствуют'
                }), 400

            book, error = DatabaseManager.update_book(book_id, data)

            if book:
                return jsonify({
                    'success': True,
                    'data': book,
                    'message': 'Книга успешно обновлена'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': error
                }), 404 if error == "Книга не найдена" else 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def delete_book(book_id):
        """DELETE /api/books/<id> - Удалить книгу"""
        try:
            success, error = DatabaseManager.delete_book(book_id)

            if success:
                return jsonify({
                    'success': True,
                    'message': 'Книга успешно удалена'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': error
                }), 404 if error == "Книга не найдена" else 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500


class UtilityHandlers:
    """Вспомогательные обработчики"""

    @staticmethod
    def get_genres():
        """GET /api/genres - Получить все жанры"""
        try:
            genres = DatabaseManager.get_all_genres()
            return jsonify({
                'success': True,
                'data': genres
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500

    @staticmethod
    def get_tags():
        """GET /api/tags - Получить все теги"""
        try:
            tags = DatabaseManager.get_all_tags()
            return jsonify({
                'success': True,
                'data': tags
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }), 500
