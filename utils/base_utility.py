import os
import subprocess

class BaseUtility:
    def __init__(self, path='.'):
        self.path = path

    @staticmethod
    def run_command(command):
        """Запускает команду через subprocess и возвращает вывод."""
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:  # Если команда завершилась с ошибкой
            return ''  # Можно вернуть пустую строку или обработать ошибку
        return result.stdout

    def file_exists(self):
        """Проверяет, существует ли файл или директория."""
        return os.path.exists(self.path)

    def create_directory(self):
        """Создает директорию, если она не существует."""
        if not os.path.exists(self.path):
            os.makedirs(self.path)