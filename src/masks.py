def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX."""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX."""
    return f"**{account_number[-4:]}"

print(get_mask_card_number("73654108430135874305"))
print(get_mask_account("73654108430135874305"))



