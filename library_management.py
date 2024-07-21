import json
import os


class Library:
    """ Создаем класс, в которой хранится коллекция книг. """
    def __init__(self, file='library.json'):
        self.file = file  # файл, в котором хранятся данные о библиотеке.
        self.books = {}  # словарь с книгами.
        self.id_counter = 1  # счетчик для генерации id книг.
        self.load_data()

    def load_data(self):
        """Загружает данные о библиотеке из файла."""
        if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.books = data.get('books', {})
                self.id_counter = data.get('id_counter', 1)
        else:
            self.books = {}
            self.id_counter = 1

    def save_data(self):
        """Сохраняет данные о библиотеке"""
        with open(self.file, 'w', encoding='utf-8') as f:  # Открывает файл для записи и преобразует данные о библиотеке
            # Записывает JSON-строку в файл и закрывает его.
            json.dump({'books': self.books, 'id_counter': self.id_counter}, f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавляет новую книгу в библиотеку"""
        book_id = self.id_counter  # Генерирует id книги и сохраняет его
        self.books[book_id] = {  # Добавляет словарь новой книги в словарь
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        self.id_counter += 1
        self.save_data()  # Сохраняет данные
        print(f'Книга добавлена: ID {book_id}, {title}.')  # Выводит сообщение о добавлении книги.

    def remove_book(self, book_id: int):
        """Удаляет книгу из библиотеки по id"""
        if book_id in self.books:  # Если книга найдена в словаре self.books, удаляет ее по ключу book_id
            del self.books[book_id]
            self.save_data()  # Сохраняет данные о библиотеке
            print(f'Книга с ID {book_id} удалена.')  # Выводит сообщение об удалении книги.
        else:
            print('Ошибка: Книга с таким ID не найдена.')

    def search_book(self, query: str) -> dict:
        """Возвращает словарь книг, в названии, авторе или годе издания"""
        results = {id: book for id, book in self.books.items() if
                   query.lower() in book['title'].lower() or
                   query.lower() in book['author'].lower() or
                   query == str(book['year'])}
        return results

    def display_books(self):
        """Выводит список всех книг в библиотеке в табличном формате."""
        if not self.books:  # Если книг нет
            print('Нет доступных книг.')
            return

        print(f"{'ID':<5} {'Название':<30} {'Автор':<25} {'Год':<10} {'Статус':<10}")# рисуем таблицу в консоле
        print("=" * 80) # рисуем таблицу в консоле
        for id, book in self.books.items(): # находим в словаре нужные книги по ключам
            print(f"{id:<5} {book['title']:<30} {book['author']:<25} {book['year']:<10} {book['status']:<10}")

    def update_book_status(self, book_id: int, new_status: str):
        """Обновляет статус книги по указанному идентификатору book_id на новый статус new_status."""
        # Если книга найдена в словаре self.books и новый статус является допустимым ("в наличии" или "выдана"),
        # обновляет статус книги.
        if book_id in self.books and new_status in ['в наличии', 'выдана']:
            self.books[book_id]['status'] = new_status
            # Сохраняет данные о библиотеке
            self.save_data()
            # Выводит сообщение об изменении статуса книги.
            print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
        else:
            print('Ошибка: Книга не найдена или статус некорректен.')


def main():
    library = Library()  # Создает экземпляр класса
    while True:  # Выводит меню с вариантами действий в цикле
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")
        # Пользователь вводит значение на выбор из меню:
        choice = input("Выберите опцию: ")

        # Если 1, то запрашиваем у пользователя данные книги (название, автор, год) и добавляет книгу в библиотеку
        if choice == '1':
            title: str = input("Введите название книги: ")
            author: str = input("Введите автора книги: ")
            year: str = input("Введите год издания: ")
            library.add_book(title, author, year)
        # Если 2, запрашиваем у пользователя id книги для удаления и удаляем книгу из библиотеки
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)
        # Если 3, запрашивает у пользователя поисковый запрос и ищет книги в библиотеке
        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_book(query)
            if results:
                print("Найденные книги:")
                for id, book in results.items():
                    print(
                        f"ID: {id}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
            else:
                print("Книги не найдены.")
        # Если 4, выводит список всех книг в библиотеке
        elif choice == '4':
            library.display_books()
        # Если 5, запрашивает у пользователя id книги и новый статус и обновляет статус книги
        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.update_book_status(book_id, new_status)
        # Если 0, выводит сообщение о выходе из программы и завершает цикл
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Ошибка: некорректный ввод, попробуйте снова.")


# Запускаем программу
if __name__ == '__main__':
    main()

