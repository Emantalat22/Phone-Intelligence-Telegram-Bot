def generate_whatsapp_link(phone):

    # Remove spaces and +
    phone = phone.replace("+", "")
    phone = phone.replace(" ", "")

    link = f"https://wa.me/{phone}"

    return link