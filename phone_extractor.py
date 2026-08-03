import re


def extract_phone_numbers(text):

    numbers = []

    patterns = [

        # International format
        r'\+\d{1,3}[\s\-().]*\d{2,4}[\s\-().]*\d{3,4}[\s\-().]*\d{3,4}',

        # Continuous international
        r'\+\d{10,15}',

        # Numbers with separators
        r'\b\d{3,4}[\s.-]\d{3,8}[\s.-]?\d{0,8}\b',

        # Continuous numbers
        r'\b\d{10,15}\b'
    ]


    for pattern in patterns:

        matches = re.findall(pattern, text)

        for number in matches:

            cleaned = re.sub(
                r'[\s\-().]',
                '',
                number
            )

            if cleaned not in numbers:
                numbers.append(cleaned)


    return numbers



def extract_phone_number(text):

    numbers = extract_phone_numbers(text)

    if numbers:
        return numbers[0]

    return None