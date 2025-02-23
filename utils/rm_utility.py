import os
import subprocess
from .base_utility import BaseUtility  # Импорт базового класса

class RmUtility(BaseUtility):
    def __init__(self, path, options=None):
        super().__init__(path)
        self.options = options if options else []

    def remove(self):
        """Удаляет файл или директорию с учетом переданных опций."""
        command = ['rm'] + self.options + [self.path]
        subprocess.run(command, check=True)

    def exists_after_removal(self):
        """Проверяет, остался ли файл/папка после удаления (для тестов)."""
        return os.path.exists(self.path)
