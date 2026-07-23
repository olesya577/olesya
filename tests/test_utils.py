from unittest.mock import mock_open, patch
from src.utils import read_json_file
import json
import logging


def setup_logging(module_name: str):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f"logs/{module_name}.log", mode="w")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


utils_logger = setup_logging('utils')


def read_json_file(file_path: str) -> list:
    """
     Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transactions_list = json.load(file)
            if isinstance(transactions_list, list):
                utils_logger.info(f"Файл {file_path} успешно прочитан.")
                return transactions_list
            else:
                utils_logger.warning(f"Содержимое файла {file_path} не является списком.")
    except FileNotFoundError:
        utils_logger.error(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        utils_logger.error(f"Ошибка декодирования JSON в файле {file_path}.")
    return []


mock_file = mock_open(
    read_data='[{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041",'
    ' "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},'
    ' "description": "Перевод организации", "from": "Maestro 1596837868705199", "to": "Счет 64686473678894779589"}]'
)


# Тест на проверку работы функции
@patch("builtins.open", mock_file)
def test_read_json_file_valid() -> None:
    with patch(
        "json.load",
        return_value=[
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            }
        ],
    ) as mock_load:
        assert read_json_file("data/operations.json") == [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            }
        ]


# Тест, если файл пуст
@patch("builtins.open", mock_file)
def test_read_json_file_empty() -> None:
    with patch("json.load", return_value=[]) as mock_load:
        assert read_json_file("data/operations.json") == []


# Тест, если файл содержит не список
@patch("builtins.open", mock_file)
def test_read_json_file_non_list() -> None:
    with patch(
        "json.load",
        return_value={
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
    ) as mock_load:
        assert read_json_file("data/operations.json") == []


# Тест, если файл не найден
@patch("builtins.open")
def test_read_json_file_not_found(mock_open):
    mock_open.side_effect = FileNotFoundError
    result = read_json_file("non_existent_file.json")
    assert result == []
