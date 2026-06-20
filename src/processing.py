from datetime import datetime
def filter_by_state(transactions_one: list, state: str = 'EXECUTED') -> list:
    """Фильтрует список словарей по значению ключа 'state'.
         Args: transactions (list): Список словарей, каждый из которых должен содержать ключ 'state'.state (str):
         Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').
         Returns: list: Новый список словарей, где значение ключа 'state' совпадает с указанным."""
    return [transaction for transaction in transactions_one if transaction.get('state') == state]
def data_list_one(date_string: str) -> datetime:
    """Парсит строку даты в формате ISO в объект datetime."""
    return datetime.fromisoformat(date_string)
# Примеры использования и проверки функций
if __name__ == "__main__":
# Тестовые данные
    test_data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}

    ]

    print("=== filter_by_state ===")
    print("По умолчанию (state='EXECUTED'):")
    result_executed = filter_by_state(test_data)
    for item in result_executed:
        print(item)

    print("\nС параметром state='CANCELED':")
    result_canceled = filter_by_state(test_data, 'CANCELED')
    for item in result_canceled:
        print(item)
    print("=== sort_by_date ===")
def sort_by_date(list_dicts_any: list[dict[str,Any]], sort_descending: bool = True) -> list[dict[str,Any]]:
    """Принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание),
    и возвращает новый список, отсортированный по дате."""
    # Преобразуем строки дат в объекты datetime для сортировки
    for date in list_dicts_any:
        date["date"] = datetime.strptime(date["date"], "%Y-%m-%dT%H:%M:%S.%f")
    # Сортируем список словарей по ключу 'date'
    sorted_data_two: list[dict[str,Any]] = sorted(list_dicts_any, key=lambda x: x["date"], reverse=sort_descending)
    # Преобразуем обратно в строковый формат
    for data in list_dicts_any:
        data["date"] = data["date"].strftime("%Y-%m-%dT%H:%M:%S.%f")
    return sorted_data_two
print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]))
