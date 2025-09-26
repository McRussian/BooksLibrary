from peewee import *
from datetime import datetime

# Создаем подключение к SQLite базе данных
database = SqliteDatabase('library.db')


# Базовая модель, от которой наследуются все остальные
class BaseModel(Model):
    class Meta:
        database = database  # Указываем базу данных для всех моделей


# Модель Автора
class Author(BaseModel):
    # Первичный ключ - автоматически увеличивающийся идентификатор
    id = AutoField(primary_key=True)

    # Имя автора (обязательное поле, максимум 100 символов)
    name = CharField(max_length=100, null=False)

    # Биография автора (может быть пустой)
    biography = TextField(null=True)

    # Дата рождения (может быть пустой)
    birth_date = DateField(null=True)

    # Страна (может быть пустой)
    country = CharField(max_length=50, null=True)

    # Когда запись была создана (автоматически при создании)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Автор: {self.name}"


# Модель Жанра
class Genre(BaseModel):
    id = AutoField(primary_key=True)

    # Название жанра (уникальное, чтобы не было дубликатов)
    name = CharField(max_length=50, unique=True)

    # Описание жанра
    description = TextField(null=True)

    def __str__(self):
        return f"Жанр: {self.name}"


# Модель Тега
class Tag(BaseModel):
    id = AutoField(primary_key=True)

    # Название тега (уникальное)
    name = CharField(max_length=30, unique=True)

    def __str__(self):
        return f"Тег: {self.name}"


# Модель Книги
class Book(BaseModel):
    id = AutoField(primary_key=True)

    # Название книги (обязательное поле)
    title = CharField(max_length=200, null=False)

    # ISBN книги (уникальный идентификатор)
    isbn = CharField(max_length=13, unique=True, null=True)

    # Год публикации
    publication_year = IntegerField(null=True)

    # Описание книги
    description = TextField(null=True)

    # Количество страниц
    page_count = IntegerField(null=True)

    # Когда книга была добавлена в базу
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Книга: {self.title}"


# Промежуточная таблица для связи "многие-ко-многим" между Книгами и Авторами
class BookAuthor(BaseModel):
    id = AutoField(primary_key=True)

    # Ссылка на книгу (внешний ключ)
    book = ForeignKeyField(Book, backref='book_authors')

    # Ссылка на автора (внешний ключ)
    author = ForeignKeyField(Author, backref='author_books')

    # Можно добавить дополнительную информацию, например, тип авторства
    authorship_type = CharField(max_length=50, default='автор')  # автор, соавтор, переводчик и т.д.


# Промежуточная таблица для связи Книг и Жанров
class BookGenre(BaseModel):
    id = AutoField(primary_key=True)
    book = ForeignKeyField(Book, backref='book_genres')
    genre = ForeignKeyField(Genre, backref='genre_books')


# Промежуточная таблица для связи Книг и Тегов
class BookTag(BaseModel):
    id = AutoField(primary_key=True)
    book = ForeignKeyField(Book, backref='book_tags')
    tag = ForeignKeyField(Tag, backref='tag_books')


# Функция для создания всех таблиц в базе данных
def create_tables():
    with database:
        # Создаем таблицы в правильном порядке (сначала основные, потом связующие)
        database.create_tables([
            Author, Genre, Tag, Book,  # Основные таблицы
            BookAuthor, BookGenre, BookTag  # Связующие таблицы
        ])
    print("Все таблицы созданы успешно!")


# Функция для заполнения базы тестовыми данными
def seed_database():
    # Создаем авторов
    authors = [
        {'name': 'Лев Толстой', 'country': 'Россия', 'birth_date': '1828-09-09'},
        {'name': 'Федор Достоевский', 'country': 'Россия', 'birth_date': '1821-11-11'},
        {'name': 'Александр Пушкин', 'country': 'Россия', 'birth_date': '1799-06-06'}
    ]

    # Создаем жанры
    genres = [
        {'name': 'Роман', 'description': 'Крупное повествовательное произведение'},
        {'name': 'Поэзия', 'description': 'Стихотворные произведения'},
        {'name': 'Драма', 'description': 'Произведения для театра'}
    ]

    # Создаем теги
    tags = [
        {'name': 'классика'},
        {'name': 'русская литература'},
        {'name': 'XIX век'}
    ]

    # Добавляем данные в базу
    with database.atomic():  # atomic гарантирует, что либо все операции выполнятся, либо ни одна
        Author.insert_many(authors).execute()
        Genre.insert_many(genres).execute()
        Tag.insert_many(tags).execute()

    print("Тестовые данные добавлены!")
