import os
from utils.base_utility import BaseUtility

class CatUtility(BaseUtility):
    def display_file(self, options=None):
        """Отображает содержимое файла, если он существует, с учетом опций."""
        if self.file_exists() and os.path.isfile(self.path):
            with open(self.path, 'r') as f:
                lines = f.readlines()

            if options is not None:
                if '-n' in options:
                    output = ''.join(f"{i + 1:5}\t{line}" for i, line in enumerate(lines))
                elif '-b' in options:
                    output = ''.join(f"{i + 1:5}\t{line}" if line.strip() else line for i, line in enumerate(lines))
                else:
                    output = ''.join(lines)
            else:
                output = ''.join(lines)

            print(output, end='')  # Убедитесь, что не добавляется лишний \n
        else:
            print(f"Файл {self.path} не существует или не является файлом.")
