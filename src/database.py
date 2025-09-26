from peewee import *
from src.models import *
import json
from playhouse.shortcuts import model_to_dict


class DatabaseManager:
    """Класс для работы с базой данных"""

    # ===== CRUD для Авторов =====

    @staticmethod
    def get_all_authors():
        """Получить всех авторов"""
        try:
            authors = Author.select().order_by(Author.name)
            return [model_to_dict(author) for author in authors]
        except Exception as e:
            print(f"Ошибка при получении авторов: {e}")
            return []

    @staticmethod
    def get_author_by_id(author_id):
        """Получить автора по ID"""
        try:
            author = Author.get_by_id(author_id)
            return model_to_dict(author)
        except Author.DoesNotExist:
            return None
        except Exception as e:
            print(f"Ошибка при получении автора {author_id}: {e}")
            return None

    @staticmethod
    def create_author(author_data):
        """Создать нового автора"""
        try:
            # Проверяем, нет ли уже автора с таким именем
            existing_author = Author.select().where(Author.name == author_data['name']).first()
            if existing_author:
                return None, "Автор с таким именем уже существует"

            # Создаем автора
            author = Author.create(**author_data)
            return model_to_dict(author), None
        except Exception as e:
            print(f"Ошибка при создании автора: {e}")
            return None, str(e)

    @staticmethod
    def update_author(author_id, author_data):
        """Обновить данные автора"""
        try:
            author = Author.get_by_id(author_id)

            # Проверяем, не пытаемся ли изменить имя на уже существующее
            if 'name' in author_data:
                existing_author = Author.select().where(
                    (Author.name == author_data['name']) &
                    (Author.id != author_id)
                ).first()
                if existing_author:
                    return None, "Автор с таким именем уже существует"

            # Обновляем поля
            for key, value in author_data.items():
                setattr(author, key, value)

            author.save()
            return model_to_dict(author), None
        except Author.DoesNotExist:
            return None, "Автор не найден"
        except Exception as e:
            print(f"Ошибка при обновлении автора {author_id}: {e}")
            return None, str(e)

    @staticmethod
    def delete_author(author_id):
        """Удалить автора"""
        try:
            author = Author.get_by_id(author_id)

            # Проверяем, есть ли у автора книги
            book_count = BookAuthor.select().where(BookAuthor.author == author_id).count()
            if book_count > 0:
                return False, f"Нельзя удалить автора, у которого есть книги ({book_count} книг)"

            author.delete_instance()
            return True, None
        except Author.DoesNotExist:
            return False, "Автор не найден"
        except Exception as e:
            print(f"Ошибка при удалении автора {author_id}: {e}")
            return False, str(e)

    # ===== CRUD для Книг =====

    @staticmethod
    def get_all_books():
        """Получить все книги с информацией об авторах, жанрах и тегах"""
        try:
            books = Book.select().order_by(Book.title)
            result = []

            for book in books:
                book_data = model_to_dict(book)

                # Получаем авторов книги
                authors = (Author
                           .select()
                           .join(BookAuthor)
                           .where(BookAuthor.book == book.id))
                book_data['authors'] = [model_to_dict(author) for author in authors]

                # Получаем жанры книги
                genres = (Genre
                          .select()
                          .join(BookGenre)
                          .where(BookGenre.book == book.id))
                book_data['genres'] = [model_to_dict(genre) for genre in genres]

                # Получаем теги книги
                tags = (Tag
                        .select()
                        .join(BookTag)
                        .where(BookTag.book == book.id))
                book_data['tags'] = [model_to_dict(tag) for tag in tags]

                result.append(book_data)

            return result
        except Exception as e:
            print(f"Ошибка при получении книг: {e}")
            return []

    @staticmethod
    def get_book_by_id(book_id):
        """Получить книгу по ID с полной информацией"""
        try:
            book = Book.get_by_id(book_id)
            book_data = model_to_dict(book)

            # Получаем авторов
            authors = (Author
                       .select()
                       .join(BookAuthor)
                       .where(BookAuthor.book == book.id))
            book_data['authors'] = [model_to_dict(author) for author in authors]

            # Получаем жанры
            genres = (Genre
                      .select()
                      .join(BookGenre)
                      .where(BookGenre.book == book.id))
            book_data['genres'] = [model_to_dict(genre) for genre in genres]

            # Получаем теги
            tags = (Tag
                    .select()
                    .join(BookTag)
                    .where(BookTag.book == book.id))
            book_data['tags'] = [model_to_dict(tag) for tag in tags]

            return book_data
        except Book.DoesNotExist:
            return None
        except Exception as e:
            print(f"Ошибка при получении книги {book_id}: {e}")
            return None

    @staticmethod
    def create_book(book_data):
        """Создать новую книгу"""
        try:
            with database.atomic():  # Все операции в одной транзакции
                # Проверяем ISBN на уникальность
                if 'isbn' in book_data and book_data['isbn']:
                    existing_book = Book.select().where(Book.isbn == book_data['isbn']).first()
                    if existing_book:
                        return None, "Книга с таким ISBN уже существует"

                # Создаем книгу (убираем поля для связей, так как их нет в модели Book)
                book_fields = {k: v for k, v in book_data.items() if k in Book._meta.fields}
                book = Book.create(**book_fields)

                # Добавляем авторов (если указаны)
                if 'author_ids' in book_data:
                    for author_id in book_data['author_ids']:
                        BookAuthor.create(book=book.id, author=author_id)

                # Добавляем жанры (если указаны)
                if 'genre_ids' in book_data:
                    for genre_id in book_data['genre_ids']:
                        BookGenre.create(book=book.id, genre=genre_id)

                # Добавляем теги (если указаны)
                if 'tag_ids' in book_data:
                    for tag_id in book_data['tag_ids']:
                        BookTag.create(book=book.id, tag=tag_id)

                return DatabaseManager.get_book_by_id(book.id), None

        except Exception as e:
            print(f"Ошибка при создании книги: {e}")
            return None, str(e)

    @staticmethod
    def update_book(book_id, book_data):
        """Обновить данные книги"""
        try:
            with database.atomic():
                book = Book.get_by_id(book_id)

                # Проверяем ISBN на уникальность (если он меняется)
                if 'isbn' in book_data and book_data['isbn'] != book.isbn:
                    existing_book = Book.select().where(
                        (Book.isbn == book_data['isbn']) &
                        (Book.id != book_id)
                    ).first()
                    if existing_book:
                        return None, "Книга с таким ISBN уже существует"

                # Обновляем поля книги
                book_fields = {k: v for k, v in book_data.items() if k in Book._meta.fields}
                for key, value in book_fields.items():
                    setattr(book, key, value)
                book.save()

                # Обновляем связи (если указаны)
                if 'author_ids' in book_data:
                    # Удаляем старых авторов
                    BookAuthor.delete().where(BookAuthor.book == book_id).execute()
                    # Добавляем новых
                    for author_id in book_data['author_ids']:
                        BookAuthor.create(book=book_id, author=author_id)

                if 'genre_ids' in book_data:
                    BookGenre.delete().where(BookGenre.book == book_id).execute()
                    for genre_id in book_data['genre_ids']:
                        BookGenre.create(book=book_id, genre=genre_id)

                if 'tag_ids' in book_data:
                    BookTag.delete().where(BookTag.book == book_id).execute()
                    for tag_id in book_data['tag_ids']:
                        BookTag.create(book=book_id, tag=tag_id)

                return DatabaseManager.get_book_by_id(book_id), None

        except Book.DoesNotExist:
            return None, "Книга не найден"
        except Exception as e:
            print(f"Ошибка при обновлении книги {book_id}: {e}")
            return None, str(e)

    @staticmethod
    def delete_book(book_id):
        """Удалить книгу"""
        try:
            with database.atomic():
                book = Book.get_by_id(book_id)

                # Удаляем все связи книги
                BookAuthor.delete().where(BookAuthor.book == book_id).execute()
                BookGenre.delete().where(BookGenre.book == book_id).execute()
                BookTag.delete().where(BookTag.book == book_id).execute()

                # Удаляем саму книгу
                book.delete_instance()
                return True, None

        except Book.DoesNotExist:
            return False, "Книга не найдена"
        except Exception as e:
            print(f"Ошибка при удалении книги {book_id}: {e}")
            return False, str(e)

    # ===== Вспомогательные методы =====

    @staticmethod
    def get_all_genres():
        """Получить все жанры"""
        try:
            genres = Genre.select().order_by(Genre.name)
            return [model_to_dict(genre) for genre in genres]
        except Exception as e:
            print(f"Ошибка при получении жанров: {e}")
            return []

    @staticmethod
    def get_all_tags():
        """Получить все теги"""
        try:
            tags = Tag.select().order_by(Tag.name)
            return [model_to_dict(tag) for tag in tags]
        except Exception as e:
            print(f"Ошибка при получении тегов: {e}")
            return []
