from config import PHONE_API_KEY

print(PHONE_API_KEY)
from lookup import get_phone_details

result = get_phone_details("+923001234567")

print(result)
