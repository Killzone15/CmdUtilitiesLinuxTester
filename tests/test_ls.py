from utils.ls_utility import LsUtility
import os
import pytest


@pytest.fixture
def setup_test_environment():
    """Подготовка тестовой среды."""
    os.mkdir('test_dir')  # Создаем директорию для теста
    with open('test_file.txt', 'w') as f:
        f.write('This is a test file.')  # Создаем тестовый файл
    yield
    # После теста удалим все, чтобы не оставлять следов
    os.remove('test_file.txt')
    os.rmdir('test_dir')


@pytest.mark.parametrize(
    'options, expected', [
        ([], ['test_file.txt', 'test_dir']),
        (['-l'], ['test_file.txt', 'test_dir']),
        (['--long'], ['test_file.txt', 'test_dir']),  # Длинная форма
        (['-a'], ['.', '..', 'test_file.txt', 'test_dir']),
        (['--all'], ['.', '..', 'test_file.txt', 'test_dir']),  # Длинная форма
        (['-al'], ['.', '..', 'test_file.txt', 'test_dir']),
        (['--all', '--long'], ['.', '..', 'test_file.txt', 'test_dir'])  # Комбинация длинных опций
    ]
)
def test_ls(options, expected, setup_test_environment):
    """Тестируем команду ls с различными опциями."""
    ls = LsUtility(path='.', options=options)  # Инициализация утилиты с переданными опциями
    result = ls.list_files()  # Выполнение команды ls
    for item in expected:
        assert item in result  # Проверка, что каждый элемент из expected есть в выводе

