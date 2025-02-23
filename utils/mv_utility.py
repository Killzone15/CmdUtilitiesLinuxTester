import shutil
import os
from utils.cp_utility import CpUtility


class MvUtility(CpUtility):
    """
    Класс для работы с утилитой mv в Linux.
    Наследуется от CpUtility, так как mv и cp имеют схожую логику работы.
    Основное отличие: после успешного перемещения файл или директория удаляются из исходного местоположения.
    """

    def __init__(self, arg1, arg2):
        super().__init__(arg1, arg2)

    def move(self, src: str, dest: str, options: str = ""):
        """Перемещает файл или директорию в новое место с учетом опций."""
        if "-n" in options or "--no-clobber" in options:
            if os.path.exists(dest):
                return
        if "-i" in options or "--interactive" in options:
            if os.path.exists(dest):
                confirmation = input(f"Перезаписать {dest}? [y/N]: ")
                if confirmation.lower() != "y":
                    return
        if "-u" in options or "--update" in options:
            if os.path.exists(dest) and os.path.getmtime(src) <= os.path.getmtime(dest):
                return
        shutil.move(src, dest)
