from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from config import BOT_TOKEN

from handlers import (
    start,
    help_command,
    handle_message,
    whatsapp_handler,
    qr_handler,
    photo_handler,
    button_handler
)

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()


    # Start command
    app.add_handler(
        CommandHandler("start", start)
    )
    #help command
    app.add_handler(
    CommandHandler("help", help_command)
)


    # WhatsApp command
    app.add_handler(
        CommandHandler("whatsapp", whatsapp_handler)
    )


    # QR command
    app.add_handler(
        CommandHandler("qr", qr_handler)
    )


    # Screenshot OCR
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )


    # Voice message
  #  app.add_handler(
   #     MessageHandler(
     #       filters.VOICE,
      #      voice_handler
      #  )
   # )


    # Buttons after OCR/Voice
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )


    # Normal phone number input
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )


    print("Bot running...")


    app.run_polling()



if __name__ == "__main__":
    main()