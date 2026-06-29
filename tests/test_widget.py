from src.widget import mask_account_card, get_date
import pytest


def test_mask_account_card(account_card):
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum  7000 79** **** 6361"
    assert mask_account_card("Счет 73654108430135874305") == "Счет  **4305"
    assert mask_account_card("Maestro 1596837868705199") == "Maestro  1596 83** **** 5199"


def test_get_date(date_time):
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2024-01-01T00:00:00.000000") == "01.01.2024"
    assert get_date("2024-12-31T23:59:59.999999") == "31.12.2024"


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        ("Некорректная строка без даты", None),
    ],
)
def test_get_date_various_formats(input_date: str, expected: str) -> None:
    if expected is None:
        with pytest.raises(ValueError):
            get_date(input_date)
    else:
        assert get_date(input_date) == expected
