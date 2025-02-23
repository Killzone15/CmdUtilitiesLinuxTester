from utils.base_utility import BaseUtility


class LsUtility(BaseUtility):
    def __init__(self, path='.', options=None):
        super().__init__(path)
        self.options = options if options else []

    def list_files(self):
        """Возвращает список файлов и директорий в указанном пути."""
        command = ['ls', self.path]

        # Преобразуем длинные опции в короткие, если необходимо
        for i, option in enumerate(self.options):
            if option == '--long':
                self.options[i] = '-l'  # Преобразуем --long в -l

        command += self.options  # Добавляем опции к команде
        return self.run_command(command)