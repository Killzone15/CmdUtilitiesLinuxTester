import pytest
import os
import shutil
import time
from utils.cp_utility import CpUtility


@pytest.fixture
def setup_test_environment():
    """Подготовка тестовой среды."""
    # Удаляем test_dir и test_dir_copy, если они существуют, для чистоты тестов
    if os.path.exists('test_dir'):
        shutil.rmtree('test_dir')
    if os.path.exists('test_dir_copy'):
        shutil.rmtree('test_dir_copy')

    os.mkdir('test_dir')  # Создаем директорию для теста
    with open('test_file.txt', 'w') as f:
        f.write('Original content')

    with open('test_dir/test_file.txt', 'w') as f:
        f.write('Inside directory')

    yield

    # Удаляем файлы и директории, если они существуют
    if os.path.exists('test_file.txt'):
        os.remove('test_file.txt')
    if os.path.exists('copy.txt'):
        os.remove('copy.txt')
    if os.path.exists('test_dir/test_file.txt'):
        os.remove('test_dir/test_file.txt')
    if os.path.exists('test_dir'):
        os.rmdir('test_dir')
    if os.path.exists('test_dir_copy'):
        shutil.rmtree('test_dir_copy')  # Удаляем копию директории


@pytest.mark.parametrize(
    'src, dst, options', [
        ('test_file.txt', 'copy.txt', []),  # Простое копирование
        ('test_dir', 'test_dir_copy', ['-r']),  # Рекурсивное копирование
        ('test_file.txt', 'copy.txt', ['-u']),  # Копирование с -u
        ('test_file.txt', 'copy.txt', ['--update']),  # Длинная форма для обновления
        ('test_dir', 'test_dir_copy', ['--recursive']),  # Длинная форма для рекурсивного копирования
        ('test_file.txt', 'copy.txt', ['--interactive']),  # Длинная форма для интерактивного копирования
    ]
)
def test_cp_options(src, dst, options, setup_test_environment):
    """Тестируем утилиту cp с разными опциями и их длинными формами."""
    cp = CpUtility(src, dst, options)
    cp.copy()

    if os.path.isdir(dst):  # Проверка для рекурсивного копирования
        assert os.path.exists(dst)  # Проверяем, что директория скопирована
    else:
        assert os.path.exists(dst)  # Проверяем, что файл скопирован


def test_cp_update(setup_test_environment):
    """Тест опции -u (копирование только если файл старее или отсутствует)."""
    with open('copy.txt', 'w') as f:
        f.write('Older content')

    # Делаем `copy.txt` старым
    old_time = time.time() - 100  # Минус 100 секунд, чтобы файл был старым
    os.utime('copy.txt', (old_time, old_time))

    cp = CpUtility('test_file.txt', 'copy.txt', options=['-u'])
    cp.copy()

    with open('copy.txt', 'r') as f:
        content = f.read()

    assert content == 'Original content'  # Файл должен обновиться
