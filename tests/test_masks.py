from src.masks import get_mask_card_number, get_mask_account

def test_get_mask_card_number(card_str):
    assert get_mask_card_number("12345678901234567890") == "1234 56** **** 7890"
    result = get_mask_card_number("   ")
    assert result == "    ** ****    "


def test_get_mask_account(account_str):
    assert get_mask_account("12345678901234567890") == "**7890"
    result = get_mask_account("1234 5678 9012 3456")
    assert result == "**3456"






