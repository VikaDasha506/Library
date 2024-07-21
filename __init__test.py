# Тестирование
import unittest
from library_management import Library
import os
import tempfile


class TestLibrary(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.library = Library(self.temp_file.name)
        self.temp_file.close()  # Закрываем временный файл, чтобы избежать блокировки

    def tearDown(self):
        # Удаляем временный файл после тестов
        os.remove(self.temp_file.name)

    def test_add_book(self):
        """Проверяет, добавление книги в библиотеку"""
        self.library.add_book("Тестовая книга", "Тестовый автор", 2023)
        self.assertEqual(len(self.library.books), 1)
        self.assertIn(1, self.library.books)
        self.assertEqual(self.library.books[1]['title'], "Тестовая книга")

    def test_remove_book(self):
        """Проверяет корректное удаление книги."""
        self.library.add_book("Тестовая книга", "Тестовый автор", 2023)
        self.library.remove_book(1)
        self.assertEqual(len(self.library.books), 0)


if __name__ == "__main__":
    unittest.main()
