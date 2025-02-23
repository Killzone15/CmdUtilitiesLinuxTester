import pytest
import os
import shutil
from utils.rm_utility import RmUtility  # Импортируем наш класс

@pytest.fixture
def setup_test_environment(tmp_path):
    """Создаёт временные файлы и папки для тестирования."""
    test_dir = tmp_path / "test_dir"
    test_file = test_dir / "test_file.txt"
    nested_dir = test_dir / "nested_dir"
    non_existent_file = tmp_path / "non_existent.txt"

    # Создаем тестовую директорию и файл
    test_dir.mkdir()
    with open(test_file, "w") as f:
        f.write("Test content")

    nested_dir.mkdir()

    return test_file, test_dir, nested_dir, non_existent_file


@pytest.mark.parametrize(
    "target, options, expected_exists",
    [
        ("test_file.txt", [], False),  # Простое удаление файла
        ("test_dir", ["-r"], False),   # Удаление директории рекурсивно (короткая нотация)
        ("test_dir", ["--recursive"], False),  # Удаление директории рекурсивно (длинная нотация)
        ("test_file.txt", ["-f"], False),  # Принудительное удаление файла (короткая нотация)
        ("test_file.txt", ["--force"], False),  # Принудительное удаление файла (длинная нотация)
        ("test_file.txt", ["-i"], True),   # Интерактивное удаление (короткая нотация, файл должен остаться)
        ("test_file.txt", ["--interactive"], True),  # Интерактивное удаление (длинная нотация, файл должен остаться)
        ("non_existent.txt", ["-f"], False),  # Принудительное удаление несуществующего файла (короткая нотация)
        ("non_existent.txt", ["--force"], False),  # Принудительное удаление несуществующего файла (длинная нотация)
    ]
)
def test_rm_options(target, options, expected_exists, setup_test_environment):
    test_file, test_dir, nested_dir, non_existent_file = setup_test_environment

    if target == "test_file.txt":
        target_path = test_file
    elif target == "test_dir":
        target_path = test_dir
    elif target == "non_existent.txt":
        target_path = non_existent_file
    else:
        pytest.fail("Invalid target")

    # Создаем тестовый файл или директорию, если они должны существовать
    if expected_exists or "-i" in options or "--interactive" in options:
        if "test_dir" in target:
            os.makedirs(target_path, exist_ok=True)
        else:
            with open(target_path, "w") as f:
                f.write("Test content")

    rm = RmUtility(str(target_path), options)
    rm.remove()

    assert target_path.exists() == expected_exists, f"{target} existence mismatch"
