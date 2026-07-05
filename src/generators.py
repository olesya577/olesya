from typing import Any, Dict, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> iter:
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> iter:
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int):
    for number in range(int(start), int(stop) + 1):
        card_number = str(number).zfill(16)  # заполняем нулями до 16 цифр
        formatted_card_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_card_number
