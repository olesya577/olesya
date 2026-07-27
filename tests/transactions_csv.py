import pytest
from src.transactions_csv import read_excel_file
from unittest.mock import Mock, patch
import pandas as pd



@patch('src.services.services_logger.error')
def test_read_from_csv(mock_error_logger):
    # Проверяем, что логгер вызван с ожидаемым сообщением
    mock_error_logger.assert_called_once()


@patch("src.utils.pd.read_excel")
def test_read_excel_file(mock_read_excel: Mock) -> None:
    # Создаем пример данных, которые будет возвращать мок
    mock_df = pd.DataFrame(
        [
            {
                "Дата операции": "19.05.2019 14:51:40",
                "Дата платежа": "21.05.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -34.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -34.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": None,
                "Категория": "Супермаркеты",
                "MCC": 5462.0,
                "Описание": "Rumyanyj Khleb Km",
                "Бонусы(включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 34.0,
            },
            {
                "Дата операции": "19.05.201914: 50:13",
                "Дата платежа": "21.05.2019",
                "Номер карты": " * 7197",
                "Статус": "OK",
                "Сумма операции": -127.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -127.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": None,
                "Категория": "Супермаркеты",
                "MCC": 5499.0,
                "Описание": "Колхоз",
                "Бонусы(включая кэшбэк)": 2,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 127.0,
            },
            {
                "Дата операции": "19.05.201914: 31:50",
                "Дата платежа": "20.05.2019",
                "Номер карты": " * 7197",
                "Статус": "OK",
                "Сумма операции": -90.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -90.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": None,
                "Категория": "Фастфуд",
                "MCC": 5814.0,
                "Описание": "IP Yakubovskaya M.V.",
                "Бонусы(включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением(": 90.0,
            },
        ]
    )
    mock_read_excel.return_value = mock_df

    # Вызываем функцию и проверяем результат
    expected_result = mock_df.to_dict(orient="records")
    result = read_excel_file("fake_path.xlsx")

    assert result == expected_result


@patch("src.utils.pd.read_excel")
def test_read_excel_file_raises_value_error(mock_read_excel: Mock) -> None:
    mock_read_excel.side_effect = ValueError("Ошибка при чтении файла Excel")
    with pytest.raises(ValueError, match="Ошибка при чтении файла Excel"):
        read_excel_file("non_existent_file.xlsx")