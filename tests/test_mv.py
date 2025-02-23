import os
import shutil
import pytest
from utils.mv_utility import MvUtility


@pytest.fixture
def setup_test_environment():
    """Фикстура для подготовки тестовой среды перед каждым тестом."""
    os.makedirs("test_src", exist_ok=True)
    os.makedirs("test_dest", exist_ok=True)
    with open("test_src/test_file.txt", "w") as f:
        f.write("Test content")
    yield
    # Очистка после тестов
    shutil.rmtree("test_dest", ignore_errors=True)
    shutil.rmtree("test_src", ignore_errors=True)
    assert not os.path.exists("test_src"), "test_src не был удален"
    assert not os.path.exists("test_dest"), "test_dest не был удален"

def recreate_test_file():
    """Создаёт тестовый файл перед каждым вызовом move()."""
    os.makedirs("test_src", exist_ok=True)
    with open("test_src/test_file.txt", "w") as f:
        f.write("Test content")

def run_mv_test(option, expected_content, monkeypatch=None):
    """Универсальная функция для тестирования разных опций mv."""
    mv_util = MvUtility("arg1_value", "arg2_value")
    recreate_test_file()
    with open("test_dest/test_file.txt", "w") as f:
        f.write("Existing content")
    if option == "-u" or option == "--update":
        os.utime("test_dest/test_file.txt", (0, 0))
    if option == "-i" or option == "--interactive":
        if monkeypatch:
            monkeypatch.setattr("builtins.input", lambda _: "n")
    mv_util.move("test_src/test_file.txt", "test_dest/test_file.txt", option)
    with open("test_dest/test_file.txt", "r") as f:
        assert f.read() == expected_content

@pytest.mark.parametrize("option", ["-n", "--no-clobber"])
def test_no_clobber(setup_test_environment, option):
    """Проверяет работу опции -n (--no-clobber)."""
    run_mv_test(option, "Existing content")

@pytest.mark.parametrize("option", ["-u", "--update"])
def test_update(setup_test_environment, option):
    """Проверяет работу опции -u (--update)."""
    run_mv_test(option, "Test content")

@pytest.mark.parametrize("option", ["-i", "--interactive"])
def test_interactive(setup_test_environment, monkeypatch, option):
    """Проверяет работу опции -i (--interactive)."""
    run_mv_test(option, "Existing content", monkeypatch)