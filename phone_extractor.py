import re

def extract_phone_number(text):

    patterns = [
        # International format: +1 (857) 555-1234
        r'\+\d{1,3}\s*\(?\d{2,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}',

        # Format: +923001234567
        r'\+\d{10,15}',

        # Format: 0300 1234567 / 0300-1234567
        r'\b\d{3,4}[\s.-]?\d{6,8}\b',

        # Format: (857) 555-1234
        r'\(\d{2,4}\)[\s.-]?\d{3}[\s.-]?\d{4}'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group()

    return None