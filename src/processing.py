from datetime import datetime

def filter_by_state(my_list_dict: list, state='EXECUTED') -> list:
    """Функция filter_by_state, которая принимает список словарей и опционально значение для ключа state (по умолчанию
    'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""
    filtered_list = []
    for dict_ in my_list_dict:
        if dict_['state'] == state:
            filtered_list.append(dict_)
    return filtered_list


def sort_by_date(list_dicts: list[dict[str, Any]], sort_descending: bool = True) -> list[dict[str, Any]]:
    """Принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание),
    и возвращает новый список, отсортированный по дате."""
    # Преобразуем строки дат в объекты datetime для сортировки
    for date in list_dicts:
        date["date"] = datetime.strptime(date["date"], "%Y-%m-%dT%H:%M:%S.%f")
    # Сортируем список словарей по ключу 'date'
    sorted_data: list[dict[str, Any]] = sorted(list_dicts, key=lambda x: x["date"], reverse=sort_descending)
    # Преобразуем обратно в строковый формат
    for data in list_dicts:
        data["date"] = data["date"].strftime("%Y-%m-%dT%H:%M:%S.%f")
    return sorted_data
