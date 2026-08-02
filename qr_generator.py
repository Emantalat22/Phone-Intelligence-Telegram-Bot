import qrcode


def create_vcard(phone_number):

    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:Phone Contact
TEL:{phone_number}
END:VCARD"""

    return vcard


def generate_contact_qr(phone_number):

    vcard_data = create_vcard(phone_number)

    qr = qrcode.make(vcard_data)

    file_name = "contact_qr.png"

    qr.save(file_name)

    return file_name