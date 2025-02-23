import os
from utils.base_utility import BaseUtility


class CatUtility(BaseUtility):
    def __init__(self, path='.'):
        super().__init__(path)

    def display_file(self):
        """Отображает содержимое файла, если он существует."""
        if self.file_exists() and os.path.isfile(self.path):
            command = ['cat', self.path]
            output = self.run_command(command)
            print(output)
        else:
            print(f"Файл {self.path} не существует или не является файлом.")