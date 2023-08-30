from datetime import datetime


def number_digits(number: int) -> int:
    digits = 0
    while number > 0:
        number //= 10
        digits += 1
    return digits


def get_first_n_digits(number: int, n: int) -> int:
    return number // (10 ** (number_digits(number) - n))


def get_last_n_digits(number: int, n: int) -> int:
    return number % (10 ** n)


def format_year_short(now: datetime) -> str:
    return now.strftime("%y")


def format_year_month(now: datetime) -> str:
    return now.strftime("%y%m")
