import re


def extract_phone_number(text):

    # Keep original text for matching
    patterns = [

        # International format:
        # +1 857 555 1234
        # +92-335-5363259
        r'\+\d{1,3}[\s\-().]*\d{2,4}[\s\-().]*\d{3,4}[\s\-().]*\d{3,4}',

        # Continuous international:
        # +923355363259
        r'\+\d{10,15}',

        # Numbers with separators:
        # 0335-536-3259
        # 0300 1234567
        r'\b\d{3,4}[\s.-]\d{3,8}[\s.-]?\d{0,8}\b',

        # Continuous numbers:
        # 03355363259
        # 8575551234
        r'\b\d{10,15}\b'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            number = match.group()

            # Clean formatting
            cleaned = re.sub(r'[\s\-().]', '', number)

            return cleaned

    return None