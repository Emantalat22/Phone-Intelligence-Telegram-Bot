from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from lookup import get_phone_details
from whatsapp import generate_whatsapp_link
from qr_generator import generate_contact_qr
from ocr import extract_text
from phone_extractor import extract_phone_number
#from voice import extract_voice_text

from language_manager import set_language, get_language



# ==========================
# START COMMAND
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="lang_english"
            ),
            InlineKeyboardButton(
                "🇵🇰 اردو",
                callback_data="lang_urdu"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Welcome to Phone Intelligence Bot\n\n"
        "Choose your language 🌐",
        reply_markup=reply_markup
    )



# ==========================
# PHONE LOOKUP HANDLER
# ==========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    language = get_language(user_id)

    phone_number = update.message.text.strip()

    result = get_phone_details(phone_number)

    if "error" in result:

        if language == "urdu":
            await update.message.reply_text(
                "❌ نمبر کی معلومات حاصل نہیں ہو سکیں۔"
            )
        else:
            await update.message.reply_text(
                "❌ Unable to fetch phone details."
            )

        return


    country = result["phone_location"]["country_name"]
    timezone = result["phone_location"]["timezone"]

    carrier = result["phone_carrier"]["name"]
    line_type = result["phone_carrier"]["line_type"]

    valid = result["phone_validation"]["is_valid"]


    if language == "urdu":

        reply = f"""
📱 فون نمبر کی معلومات

🌍 ملک: {country or 'نامعلوم'}
📡 نیٹ ورک: {carrier or 'نامعلوم'}
📱 قسم: {line_type or 'نامعلوم'}
✅ درست: {valid}
⏰ ٹائم زون: {timezone or 'نامعلوم'}
"""

    else:

        reply = f"""
📱 Phone Number Details

🌍 Country: {country or 'Unknown'}
📡 Carrier: {carrier or 'Unknown'}
📱 Type: {line_type or 'Unknown'}
✅ Valid: {valid}
⏰ Timezone: {timezone or 'Unknown'}
"""


    await update.message.reply_text(reply)



# ==========================
# WHATSAPP COMMAND
# ==========================

async def whatsapp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    phone = text.replace("/whatsapp", "").strip()


    if not phone:

        await update.message.reply_text(
            "Please send number like:\n/whatsapp +923001234567"
        )

        return


    link = generate_whatsapp_link(phone)


    await update.message.reply_text(
        f"💬 WhatsApp Link:\n{link}"
    )



# ==========================
# QR COMMAND
# ==========================

async def qr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    phone = text.replace("/qr", "").strip()


    if not phone:

        await update.message.reply_text(
            "Please send number like:\n/qr +923001234567"
        )

        return


    qr_file = generate_contact_qr(phone)


    await update.message.reply_photo(
        photo=open(qr_file, "rb"),
        caption="📇 Contact QR Generated\n\nScan this QR code to save the contact."
    )



# ==========================
# IMAGE OCR HANDLER
# ==========================

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1]

    file = await photo.get_file()

    image_path = "received_image.jpg"

    await file.download_to_drive(image_path)


    text = extract_text(image_path)

    phone = extract_phone_number(text)
    print("OCR TEXT:")
    print(text)

    print("DETECTED PHONE:")
    print(phone)


    if phone:

        keyboard = [

            [
                InlineKeyboardButton(
                    "🔍 Lookup Details",
                    callback_data=f"lookup_{phone}"
                )
            ],

            [
                InlineKeyboardButton(
                    "💬 WhatsApp",
                    callback_data=f"whatsapp_{phone}"
                )
            ],

            [
                InlineKeyboardButton(
                    "📇 Generate QR",
                    callback_data=f"qr_{phone}"
                )
            ]

        ]


        reply_markup = InlineKeyboardMarkup(keyboard)


        await update.message.reply_text(
            f"📱 Phone Number Detected:\n\n"
            f"{phone}\n\n"
            "Choose an action:",
            reply_markup=reply_markup
        )


    else:
     await update.message.reply_text(
        "❌ No phone number found in this image."
    )
# ==========================
# BUTTON HANDLER
# ==========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id


    # ==========================
    # LANGUAGE SELECTION
    # ==========================

    if data == "lang_english":

        set_language(user_id, "english")

        await query.edit_message_text(
            "✅ Language selected: English"
        )

        return


    elif data == "lang_urdu":

        set_language(user_id, "urdu")

        await query.edit_message_text(
            "✅ زبان منتخب کی گئی: اردو"
        )

        return



    # ==========================
    # LOOKUP BUTTON
    # ==========================

    if data.startswith("lookup_"):

        phone = data.replace("lookup_", "")

        result = get_phone_details(phone)


        if "error" in result:

            await query.message.reply_text(
                "❌ Unable to fetch details."
            )

            return



        country = result["phone_location"]["country_name"]
        timezone = result["phone_location"]["timezone"]

        carrier = result["phone_carrier"]["name"]
        line_type = result["phone_carrier"]["line_type"]

        valid = result["phone_validation"]["is_valid"]



        language = get_language(user_id)



        if language == "urdu":

            reply = f"""
📱 فون نمبر کی معلومات

🌍 ملک: {country or 'نامعلوم'}
📡 نیٹ ورک: {carrier or 'نامعلوم'}
📱 قسم: {line_type or 'نامعلوم'}
✅ درست: {valid}
⏰ ٹائم زون: {timezone or 'نامعلوم'}
"""


        else:

            reply = f"""
📱 Phone Number Details

🌍 Country: {country or 'Unknown'}
📡 Carrier: {carrier or 'Unknown'}
📱 Type: {line_type or 'Unknown'}
✅ Valid: {valid}
⏰ Timezone: {timezone or 'Unknown'}
"""


        await query.message.reply_text(reply)




    # ==========================
    # WHATSAPP BUTTON
    # ==========================

    elif data.startswith("whatsapp_"):

        phone = data.replace("whatsapp_", "")

        link = generate_whatsapp_link(phone)


        await query.message.reply_text(
            f"💬 WhatsApp Link:\n{link}"
        )




    # ==========================
    # QR BUTTON
    # ==========================

    elif data.startswith("qr_"):

        phone = data.replace("qr_", "")


        qr_file = generate_contact_qr(phone)


        await query.message.reply_photo(
            photo=open(qr_file, "rb"),
            caption="📇 Contact QR Generated"
        )




# ==========================
# VOICE HANDLER
# ==========================

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("VOICE MESSAGE RECEIVED")


    voice = update.message.voice


    file = await context.bot.get_file(
        voice.file_id
    )


    audio_path = "voice_message.ogg"


    await file.download_to_drive(audio_path)



    text = extract_voice_text(audio_path)


    phone = extract_phone_number(text)



    if phone:


        keyboard = [

            [
                InlineKeyboardButton(
                    "🔍 Lookup Details",
                    callback_data=f"lookup_{phone}"
                )
            ],

            [
                InlineKeyboardButton(
                    "💬 WhatsApp",
                    callback_data=f"whatsapp_{phone}"
                )
            ],

            [
                InlineKeyboardButton(
                    "📇 Generate QR",
                    callback_data=f"qr_{phone}"
                )
            ]

        ]


        reply_markup = InlineKeyboardMarkup(keyboard)



        await update.message.reply_text(

            f"🎙️ Voice Converted:\n\n"
            f"📱 Phone Number Detected:\n{phone}\n\n"
            "Choose an action:",

            reply_markup=reply_markup
        )



    else:


        await update.message.reply_text(

            f"🎙️ Voice Text:\n\n{text}\n\n"
            "❌ No phone number detected."

        )
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Phone Intelligence Bot Help\n\n"
        "📱 Send a phone number:\n"
        "→ Get country, carrier, type, validity and timezone\n\n"
        "💬 /whatsapp +number\n"
        "→ Generate WhatsApp link\n\n"
        "📇 /qr +number\n"
        "→ Generate contact QR code\n\n"
        "🖼 Send an image:\n"
        "→ Extract phone numbers from screenshots\n\n"
        "🎙 Send a voice message:\n"
        "→ Convert voice into phone number\n\n"
        "🌐 Choose language using /start"
    )