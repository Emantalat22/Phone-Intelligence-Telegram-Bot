import re


def extract_phone_number(text):

    numbers = re.findall(
        r'(\+?\d[\d\s-]{8,}\d)',
        text
    )

    if numbers:
        phone = numbers[0]

        # remove spaces and hyphens
        phone = phone.replace(" ", "")
        phone = phone.replace("-", "")

        return phone

    return None