from unittest.mock import mock_open, patch

from src.utils import read_json_file

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
