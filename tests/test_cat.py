import os
import tempfile
import pytest
from utils.cat_utility import CatUtility  # Импортируйте ваш класс CatUtility

@pytest.fixture
def temp_file():
    """Создает временный файл для тестов."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'Line 1\nLine 2\nLine 3\n')
        f.flush()  # Убедитесь, что данные записаны
        yield f.name
    os.remove(f.name)

@pytest.fixture
def temp_files():
    """Создает несколько временных файлов для тестов объединения."""
    file_names = []
    for i in range(2):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(f'File {i + 1} Line 1\n'.encode())
            f.write(f'File {i + 1} Line 2\n'.encode())
            f.flush()
            file_names.append(f.name)
    yield file_names
    for file_name in file_names:
        os.remove(file_name)

def test_display_file(temp_file, capsys):
    cat_util = CatUtility(temp_file)
    cat_util.display_file()  # Вызываем метод display_file
    captured = capsys.readouterr()  # Захватываем вывод
    expected_output = 'Line 1\nLine 2\nLine 3\n'
    # Проверяем, что вывод соответствует ожидаемому
    assert captured.out == expected_output

def test_display_multiple_files(temp_files, capsys):
    cat_util = CatUtility()
    for file in temp_files:
        cat_util.path = file
        cat_util.display_file()  # Вызываем метод display_file
    captured = capsys.readouterr()  # Захватываем вывод
    expected_output = (
        'File 1 Line 1\n'
        'File 1 Line 2\n'
        'File 2 Line 1\n'
        'File 2 Line 2\n'
    )
    # Проверяем, что вывод нескольких файлов соответствует ожидаемому
    assert captured.out == expected_output

@pytest.mark.parametrize("options, expected_output", [
    (['-n'], '    1\tLine 1\n    2\tLine 2\n    3\tLine 3\n'),
    (['-b'], '    1\tLine 1\n    2\tLine 2\n    3\tLine 3\n'),
])
def test_display_file_with_options(temp_file, options, expected_output, capsys):
    cat_util = CatUtility(temp_file)
    cat_util.display_file(options)  # Используем метод display_file с опциями
    captured = capsys.readouterr()  # Захватываем вывод
    assert captured.out == expected_output  # Проверяем вывод
