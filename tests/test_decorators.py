import os

import pytest

from src.decorators import log

from typing import Any


@log()
def divide_function_console(x: float, y: float) -> float:
    return x / y


@pytest.mark.parametrize(
    "x, y, expected_output",
    [
        (3, 2, "divide_function_console ok"),
        (1, 0, "divide_function_console error: ZeroDivisionError. Inputs: (1, 0), {}"),
    ],
)
def test_log_to_console(capsys: Any, x: float, y: float, expected_output: str) -> None:
    if y == 0:
        with pytest.raises(ZeroDivisionError):
            divide_function_console(x, y)
    else:
        divide_function_console(x, y)
    captured = capsys.readouterr()
    assert expected_output in captured.out


@pytest.mark.parametrize(
    "x, y, expected_output",
    [(3, 2, "divide_function_file ok"), (1, 0, "divide_function_file error: ZeroDivisionError. Inputs: (1, 0), {}")],
)
def divide_function_file(x: float, y: float) -> float:
    log_file = "test_log.txt"

    # Удаляем файл перед тестом, если он существует
    if os.path.exists(log_file):
        os.remove(log_file)

    if y == 0:
        with pytest.raises(ZeroDivisionError):
            divide_function_file(x, y)
    else:
        divide_function_file(x, y)

    # Проверяем, что файл создан и содержит ожидаемое сообщение
    with open(log_file, "r") as f:
        content = f.read()
        assert "expected_output" in content

    # Удаляем файл после теста
    if os.path.exists(log_file):
        os.remove(log_file)


@log(filename="test_log.txt")
def divide_function_file(x, y):
    return x / y
