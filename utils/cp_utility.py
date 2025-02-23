from utils.base_utility import BaseUtility
import shutil
import os

class CpUtility(BaseUtility):
    def __init__(self, src, dst, options=None):
        super().__init__(src)  # Инициализация базового класса с исходным файлом или директорией
        self.destination = dst
        self.options = options or []

    def copy(self):
        """Копирует файл или директорию в указанное место."""
        if self.file_exists():  # Проверка существования файла или директории
            if os.path.isdir(self.path):
                if '--recursive' in self.options or '-r' in self.options:
                    shutil.copytree(self.path, self.destination)
                    print(f"Directory copied from {self.path} to {self.destination}.")
                else:
                    raise ValueError("Cannot copy a directory without the recursive option.")
            else:
                shutil.copy2(self.path, self.destination)
                print(f"File copied from {self.path} to {self.destination}.")
        else:
            raise FileNotFoundError(f"{self.path} does not exist.")
