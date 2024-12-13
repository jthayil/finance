import re

def remove_office(value):
    pattern = r"(B\.O|S\.O|H\.O|BO|SO|HO)"
    actual_value = re.sub(pattern, '', value)
    return actual_value.strip().title()


def itsEmailID(mail):
    mail_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(mail_regex, mail):
        return True
    return False


ones = [
    "",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve",
    "Thirteen",
    "Fourteen",
    "Fifteen",
    "Sixteen",
    "Seventeen",
    "Eighteen",
    "Nineteen",
]

tens = [
    "",
    "",
    "Twenty",
    "Thirty",
    "Forty",
    "Fifty",
    "Sixty",
    "Seventy",
    "Eighty",
    "Ninety",
]

thousands = ["", "thousand", "million", "billion", "trillion"]


def convert_whole_number_to_words(n):
    if n == 0:
        return "zero"

    words = []
    group = 0

    # Process each group of 3 digits
    while n > 0:
        if n % 1000 != 0:
            words.insert(
                0,
                convert_group_to_words(n % 1000)
                + (f" {thousands[group]}" if thousands[group] else ""),
            )
        n //= 1000
        group += 1

    return " ".join(words).strip()


def convert_group_to_words(n):
    """Convert numbers less than 1000 to words."""
    words = []

    if n >= 100:
        words.append(ones[n // 100] + " Hundred")
        n %= 100

    if n >= 20:
        words.append(tens[n // 10])
        n %= 10

    if n > 0:
        words.append(ones[n])

    return " ".join(words).strip()


def convert_to_words(amount):
    if isinstance(amount, float):
        whole_part, decimal_part = str(amount).split(".")
    else:
        whole_part = str(amount)
        decimal_part = "00"

    whole_part_in_words = convert_whole_number_to_words(int(whole_part))

    if decimal_part != "00":
        decimal_in_words = convert_whole_number_to_words(int(decimal_part))
        return f"{whole_part_in_words} Rupees and {decimal_in_words} Paise"
    else:
        return f"{whole_part_in_words} Rupees"


# eof
