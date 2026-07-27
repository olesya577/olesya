from src.masks import get_mask_card_number, get_mask_account

import logging


logger = logging.getLogger('masks_log')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/masks_log.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Функция маскировки
from src.decorators import log
@log(filename="mylog.txt")
#logger = setup_logging('masks_log')
def get_mask_card_number(card_number: str) -> str:
    logger.info('Ввод номера карты клиента')
    result = ""
    card_number_new = card_number.replace(" ", "").replace("-", "")

    if len(card_number_new) != 16 or card_number_new.isdigit() is False:
        logger.error("Введен некорректный номер карты")
        result = "Введен некорректный номер карты"
    else:
        result = f"{card_number_new[:4]} {card_number_new[4:6]}** **** {card_number_new[-4:]}"
    return result


print(get_mask_card_number(card_number="12345678901234567890"))


@log(filename="mylog.txt")
def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    logger.info('Ввод номера счета клиента')
    if len(account_number) != 20 or not account_number.isdigit():
        logger.error("Введен некорректный номер банковского счета")
        return "Введён некорректный номер банковского счёта (должно быть 20 цифр)."
    return f"**** **** **** **** {account_number[-4:]}"


print(get_mask_account(account_number="12345678901234567890"))


def test_get_mask_card_number(card_str):
    assert get_mask_card_number("12345678901234567890") == "1234 56** **** 7890"
    result = get_mask_card_number("   ")
    assert result == "   ** ****    "


def test_get_mask_account(account_str):
    assert get_mask_account("12345678901234567890") == "**7890"
    result = get_mask_account("1234 5678 9012 3456")
    assert result == "**7890"


