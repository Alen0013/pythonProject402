import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict

# Singleton для логгера
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            logging.basicConfig(filename='library.log', level=logging.INFO)
            cls._instance.logger = logging.getLogger("LibraryLogger")
        return cls._instance

    def log(self, message: str):
        self.logger.info(message)

# Factory Method для создания сущностей
class EntityFactory(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

class BookFactory(EntityFactory):
    def create(self, **kwargs):
        return Book(**kwargs)

class LibrarianFactory(EntityFactory):
    def create(self, **kwargs):
        return Librarian(**kwargs)

class ReaderFactory(EntityFactory):
    def create(self, **kwargs):
        return Reader(**kwargs)

# Сущности
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        return f"Book: {self.title} by {self.author}, ISBN: {self.isbn}"

class Librarian:
    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id

    def __str__(self):
        return f"Librarian: {self.name}, ID: {self.employee_id}"

class Reader:
    def __init__(self, name: str, reader_id: str):
        self.name = name
        self.reader_id = reader_id

    def __str__(self):
        return f"Reader: {self.name}, ID: {self.reader_id}"

# Observer для уведомлений
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class LibraryObserver(Observer):
    def __init__(self):
        self.logger = Logger()

    def update(self, message: str):
        self.logger.log(message)

# Command для операций
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddBookCommand(Command):
    def __init__(self, library, book):
        self.library = library
        self.book = book

    def execute(self):
        self.library.add_book(self.book)

class RemoveBookCommand(Command):
    def __init__(self, library, isbn):
        self.library = library
        self.isbn = isbn

    def execute(self):
        self.library.remove_book(self.isbn)

# Memento для сохранения состояния
class LibraryMemento:
    def __init__(self, state):
        self.state = state

class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.observers: List[Observer] = []
        self.logger = Logger()

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)

    def add_book(self, book: Book):
        self.books[book.isbn] = book
        self.notify_observers(f"Added book: {book.title}")

    def remove_book(self, isbn: str):
        if isbn in self.books:
            book = self.books.pop(isbn)
            self.notify_observers(f"Removed book: {book.title}")

    def save_state(self):
        return LibraryMemento(json.dumps([book.__dict__ for book in self.books.values()]))

    def restore_state(self, memento: LibraryMemento):
        self.books = {book['isbn']: Book(**book) for book in json.loads(memento.state)}

    def search_books(self, strategy, query):
        return strategy.search(self.books, query)

# Strategy для поиска
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books: Dict[str, Book], query: str) -> List[Book]:
        pass

class TitleSearchStrategy(SearchStrategy):
    def search(self, books: Dict[str, Book], query: str) -> List[Book]:
        return [book for book in books.values() if query.lower() in book.title.lower()]

class AuthorSearchStrategy(SearchStrategy):
    def search(self, books: Dict[str, Book], query: str) -> List[Book]:
        return [book for book in books.values() if query.lower() in book.author.lower()]

# Пример использования
if __name__ == "__main__":
    library = Library()
    observer = LibraryObserver()
    library.add_observer(observer)

    book_factory = BookFactory()
    book1 = book_factory.create(title="1984", author="George Orwell", isbn="123456")
    book2 = book_factory.create(title="Brave New World", author="Aldous Huxley", isbn="654321")

    add_book_command = AddBookCommand(library, book1)
    add_book_command.execute()

    remove_book_command = RemoveBookCommand(library, "654321")
    remove_book_command.execute()

    memento = library.save_state()
    library.restore_state(memento)

    title_search = TitleSearchStrategy()
    results = library.search_books(title_search, "1984")
    for result in results:
        print(result)