from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = 7668929986:AAGT3F1JBSU4rgMp-XMofNFRPoSapZu9Bro

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Español", callback_data="lang_es"),
            InlineKeyboardButton("English", callback_data="lang_en")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "**PNP Television on Telegram**\n\nEscoge tu idioma | Chose your language",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "lang_es":
        keyboard = [
            [InlineKeyboardButton("Planes de membresía", callback_data="menu_planes")],
            [InlineKeyboardButton("Ingreso de Miembros", callback_data="menu_miembros")],
            [InlineKeyboardButton("PNP Television en Zoom", callback_data="menu_zoom_es")],
            [InlineKeyboardButton("PNP Television App", callback_data="menu_app_es")],
            [InlineKeyboardButton("Contáctenos", callback_data="menu_contacto")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "**¡Bienvenid@ a PNP Television!**\n\n"
            "La comunidad más grande en Telegram para amantes del crico. Estás interactuando con nuestro chatbot, el cual te permitirá:\n\n"
            "1. Suscribirte a nuestros servicios premium\n"
            "2. Contactar con atención al cliente\n"
            "3. Conocer más sobre nuestro proyecto\n\n"
            "Solo haz clic en los botones del menú inferior y disfruta tu visita.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("English version coming soon!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_language, pattern="^lang_"))

    app.run_polling()

if __name__ == "__main__":
    main()
# Menú principal en inglés (callback "lang_en")
async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lang_es":
        keyboard = [
            [InlineKeyboardButton("Planes de membresía", callback_data="menu_planes")],
            [InlineKeyboardButton("Ingreso de Miembros", callback_data="menu_miembros")],
            [InlineKeyboardButton("PNP Television en Zoom", callback_data="menu_zoom_es")],
            [InlineKeyboardButton("PNP Television App", callback_data="menu_app_es")],
            [InlineKeyboardButton("Contáctenos", callback_data="menu_contacto")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "**¡Bienvenid@ a PNP Television!**\n\n"
            "La comunidad más grande en Telegram para amantes del crico. Estás interactuando con nuestro chatbot, el cual te permitirá:\n\n"
            "1. Suscribirte a nuestros servicios premium\n"
            "2. Contactar con atención al cliente\n"
            "3. Conocer más sobre nuestro proyecto\n\n"
            "Solo haz clic en los botones del menú inferior y disfruta tu visita.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "lang_en":
        keyboard = [
            [InlineKeyboardButton("Membership Plans", callback_data="menu_planes_en")],
            [InlineKeyboardButton("Member Access", callback_data="menu_miembros_en")],
            [InlineKeyboardButton("PNP Television on Zoom", callback_data="menu_zoom_en")],
            [InlineKeyboardButton("PNP Television App", callback_data="menu_app_en")],
            [InlineKeyboardButton("Contact Us", callback_data="menu_contact_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "**Welcome to PNP Television!**\n\n"
            "The largest Telegram community for PNP lovers. You’re now interacting with our chatbot, which allows you to:\n\n"
            "1. Subscribe to our premium services\n"
            "2. Contact customer support\n"
            "3. Learn more about our project\n\n"
            "Just click the buttons below to start your journey.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
