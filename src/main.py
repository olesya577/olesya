import re
from typing import List, Dict, Any
from collections import Counter
import os
from src.generators import filter_by_currency
from src.utils import read_json_file
from src.processing import filter_by_state, sort_by_date
from src.transactions_csv import read_from_csv, read_excel_file
from src.widget import get_date
from src.masks import get_mask_account

# Получение текущего рабочего каталога
current_directory = os.getcwd()

# Создание полного пути к файлу
file_path = os.path.join(current_directory, "src", "transactions.csv")


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список банковских операций по строке поиска в описании операции.
    Предполагается, что каждый словарь в списке `data` содержит ключ 'description' (описание),
    в котором может встречаться искомая строка.
    *Используется модуль `re` для поиска с учётом нечувствительности к регистру.*
    Параметры:
    - data: список словарей с данными операций
    - search: строка поиска
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    # Фильтруем данные: проверяем, есть ли совпадение в поле 'description'
    result = [
        operation for operation in data if "description" in operation and pattern.search(operation["description"])
    ]

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций в каждой из заданных категорий.
    Категории определяются по вхождению строки из `categories`
    в поле `description` каждой операции (регистра независимо).
    *Используется `Counter` для эффективного подсчёта.*
    Параметры:
    - data: список словарей с данными операций (обязательно с полем 'description')
    - categories: список строк — названия категорий для поиска
    Возвращает:
    - словарь: ключ — категория, значение — количество операций, где она найдена
    """
    # Список для хранения найденных категорий по каждой операции
    matched_categories = []

    # Приводим категории к нижнему регистру для регистра независимого поиска
    lower_categories = [cat.lower() for cat in categories]

    for operation in data:
        desc = operation.get("description", "").lower()
        # Проверяем, к какой категории относится описание
        for cat in lower_categories:
            if cat in desc:
                matched_categories.append(cat)
                break  # Операция относится только к одной категории (первая найденная)

    # Считаем количество по каждой категории
    counts = Counter(matched_categories)
    # Возвращаем обычный словарь, включая категории с нулём, если нужно их явно указать
    return {cat: counts.get(cat.lower(), 0) for cat in categories}


def main():
    """
     Предоставляет пользовательский интерфейс, отвечает за основную логику проекта с пользователем,
    связывает функциональности между собой.
    """
    transactions = []

    while True:
        print("\nПривет!\nДобро пожаловать в программу работы с банковскими транзакциями.\n")
        print(
            "Выберите необходимый пункт меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла:"
        )
        users_choice = (input("\nВаш выбор: ")).strip()
        if users_choice == "1":
            print("Для обработки выбран JSON-файл.")
            file_path = "../data/operations.json"
            transactions = read_json_file(file_path)
            break
        elif users_choice == "2":
            print("Для обработки выбран CSV-файл.")
            path_csv = "../data/transactions.csv"
            transactions = read_from_csv(path_csv)
            break
        elif users_choice == "3":
            print("Для обработки выбран XLSX-файл.")
            path_excel = "../data/transactions_excel.xlsx"
            transactions = read_excel_file(path_excel)
            break
        else:
            print("\nНеверный выбор. Выберите 1,2 или 3")
            continue
    while True:
        print(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        state = ["EXECUTED", "CANCELED", "PENDING"]
        user_status = input("\nВаш выбор: ").strip().upper()
        if user_status in state:
            print(f"Был выбран статус: {user_status}")
            transactions = filter_by_state(transactions, user_status)
            break
        else:
            print(f'Статус операции "{user_status}" недоступен')
            continue

    while True:
        sort_by_date_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
        if sort_by_date_choice == "да":
            order_choice = (
                input("Отсортировать по возрастанию или по убыванию?\n" 'Введите "по возрастанию" или "по убыванию"\n')
                .strip()
                .lower()
            )
            if order_choice == "по возрастанию":
                transactions = sort_by_date(transactions, reverse=False)
                break
            elif order_choice == "по убыванию":
                transactions = sort_by_date(transactions, reverse=True)
                break
        elif sort_by_date_choice == "нет":
            break
        else:
            print(f'Ввод "{sort_by_date_choice}" некорректен . Наберите Да или Нет')
            continue

    rub_filter = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if rub_filter == "да":
        if users_choice == "1":
            transactions = list(filter_by_currency(transactions, "RUB", from_json=True))
        else:
            transactions = list(filter_by_currency(transactions, "RUB", from_json=False))

    word_filter = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip()
    if word_filter == "да":
        search_word = input("Введите слово для фильтрации транзакций по описанию: ")
        transactions = process_bank_search(transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        date = get_date(transaction["date"])
        description = transaction["description"]
        from_account = get_mask_account(transaction.get("from", ""))
        to_account = get_mask_account(transaction.get("to", ""))
        if users_choice == "1":
            amount = transaction["operationAmount"]["amount"]
            currency = transaction["operationAmount"]["currency"]["name"]
        else:
            amount = transaction["amount"]
            currency = transaction["currency_name"]

        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
        print(f"Сумма: {amount} {currency}\n")


main()
