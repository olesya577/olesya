import pytest


@pytest.fixture
def card_str():
    return [
        ("12345678901234567890", "**7890"),
        ("1234567890", "**7890"),
        ("12345678", "**5678"),
        ("1234", "**1234"),
        ("123", "**123"),
        ("12", "**12"),
        ("1", "**1"),
        ("", "**"),
        ("1234 5678", "**5678"),
        ("1234-5678", "**5678"),
        ("ABC123", "**B123"),
        ("00001234", "**1234"),
        ("12340000", "**0000"),
    ]


@pytest.fixture
def account_str():
    return [
        ("12345678901234567890", "**7890"),
        ("1234567890", "**7890"),
        ("12345678", "**5678"),
        ("1234", "**1234"),
        ("123", "**123"),
        ("12", "**12"),
        ("1", "**1"),
        ("", "**"),
        ("1234 5678", "**5678"),
        ("1234-5678", "**5678"),
        ("ABC123", "**B123"),
        ("00001234", "**1234"),
        ("12340000", "**0000"),
    ]


@pytest.fixture
def account_card():
    return "Visa Platinum 159683786870519"


@pytest.fixture
def date_time():
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2023-01-14T15:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-13T08:45:00"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-12T12:00:00"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-11T09:20:00"},
    ]


@pytest.fixture
def sample_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2023-01-15T10:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15T10:00:00"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-15T10:00:00"},
    ]
