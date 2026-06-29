from src.processing import filter_by_state, sort_by_date
import pytest

def test_filter_by_executed_state(sample_data):
    """Фильтрация по статусу 'EXECUTED'"""
    result = filter_by_state(sample_data)
    expected = [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-15T10:00:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-13T08:45:00'},
        {'id': 5, 'state': 'EXECUTED', 'date': '2023-01-11T09:20:00'},
    ]
    assert result == expected
    assert len(result) == 3


def test_filter_by_canceled_state(sample_data):
    """ Фильтрация по статусу 'CANCELED'"""
    result = filter_by_state(sample_data, 'CANCELED')
    expected = [{'id': 4, 'state': 'CANCELED', 'date': '2023-01-12T12:00:00'},]
    assert result == expected
    assert len(result) == 1

def test_filter_by_pending_state(sample_data):
    """ Фильтрация по статусу 'PENDING'"""
    result = filter_by_state(sample_data, 'PENDING')
    expected = [{'id': 2, 'state': 'PENDING', 'date': '2023-01-14T15:30:00'},]
    assert result == expected
    assert len(result) == 1

def test_filter_with_no_matching_state(sample_data):
    """ Отсутствие словарей с указанным статусом"""
    data = [{'id': 1, 'state': 'PENDING', 'date': '2023-01-15T10:00:00'},
            {'id': 2, 'state': 'PENDING', 'date': '2023-01-14T15:30:00'},]
    result = filter_by_state(data, 'EXECUTED')
    assert result == []
    assert len(result) == 0


@pytest.mark.parametrize("test_data,state,expected_count,expected_ids", [
    # Пустые данные
    ([], 'EXECUTED', 0, []),
    ([], 'PENDING', 0, []),

    # Данные только с одним статусом
    ([
         {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-15T10:00:00'},
         {'id': 2, 'state': 'EXECUTED', 'date': '2023-01-14T15:30:00'},
     ], 'EXECUTED', 2, [1, 2]),

    # Данные без нужного статуса
    ([
         {'id': 1, 'state': 'PENDING', 'date': '2023-01-15T10:00:00'},
         {'id': 2, 'state': 'CANCELED', 'date': '2023-01-14T15:30:00'},
     ], 'EXECUTED', 0, []),
])
def test_filter_by_state_parametrized(test_data, state, expected_count, expected_ids):
    """Параметризованные тесты для различных статусов"""
    result = filter_by_state(test_data, state)
    assert len(result) == expected_count
    if expected_ids:
        result_ids = [item['id'] for item in result]
        assert result_ids == expected_ids


def test_filter_by_nonexistent_state(sample_data):
    """ Фильтрация по несуществующему статусу (должна вернуть пустой список)"""
    result = filter_by_state(sample_data, 'UNKNOWN')
    assert result == []
    assert len(result) == 0


def test_sort_with_single_item(sample_dates):
    """ Сортировка с одним элементом"""
    data = [{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-15T10:00:00'}]
    result = sort_by_date(data)
    assert result == data
    assert len(result) == 1


def test_sort_with_empty_list(sample_dates):
    """ Сортировка пустого списка"""
    result = sort_by_date([])
    assert result == []
    assert len(result) == 0


def test_sort_descending_default(sample_data):
    """ Сортировка по убыванию (по умолчанию)"""
    result = sort_by_date(sample_data)
    expected = [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-15T10:00:00'},
        {'id': 2, 'state': 'PENDING', 'date': '2023-01-14T15:30:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-13T08:45:00'},
        {'id': 4, 'state': 'CANCELED', 'date': '2023-01-12T12:00:00'},
        {'id': 5, 'state': 'EXECUTED', 'date': '2023-01-11T09:20:00'},]
    assert result == expected

def test_sort_with_same_dates(sample_dates):
    """ Сортировка при одинаковых датах"""
    result = sort_by_date(sample_dates)
    # Порядок при одинаковых датах может быть любым, проверяем только даты
    dates = [item['date'] for item in result]
    assert all(date == '2023-01-15T10:00:00' for date in dates)
    assert len(result) == 4


