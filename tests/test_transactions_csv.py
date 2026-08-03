from src.transactions_csv import read_excel_file, read_from_csv
from unittest.mock import patch, Mock


@patch("csv.DictReader")
def test_success(mock_reader):
    mock_reader.return_value = [{"id": "1"}]


result = read_from_csv("test.csv")


@patch("pandas.read_excel")
def test_excel(mock_read):
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1}]
    mock_read.return_value = mock_df


result = read_excel_file("test.xlsx")


@patch("pandas.read_excel")
def test_read_excel_success(mock_read_excel):
    """Тест успешное чтение Excel-файла"""
    # Создаем мок-DataFrame
    mock_df = Mock()
    mock_df.where.return_value = mock_df
    mock_df.to_dict.return_value = [
        {"id": 1, "amount": 100.50, "date": "2023-01-15"},
        {"id": 2, "amount": 200.75, "date": "2023-01-14"},
        {"id": 3, "amount": 300.00, "date": "2023-01-13"},
    ]

    mock_read_excel.return_value = mock_df

    result = read_excel_file("test.xlsx")

    # Проверяем вызовы
    mock_read_excel.assert_called_once_with("test.xlsx")
    mock_df.where.assert_called_once()
    mock_df.to_dict.assert_called_once_with(orient="records")

    # Проверяем результат
    assert len(result) == 3
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 100.50
