import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ——— Constantes ———
TOKEN = "7899263814:AAFfIAxbqwscUUZgEgXcPLCfcH9g53dtpoE"
ADMIN_ID = 7483956865
BOLD_IDENTITY_KEY = "LgANsB3U4Qsr1hWWG3dBFXdxPZd4VheS-bvuk2Vzi7E"

# ← justo antes de esto…
PLAN_LINK_IDS = {
    "Trial Trip":           "LNK_T9BOR6N1GU",   # Week Pass
    "Monthly Adventure":    "LNK_C2TVYWCTHJ",   # Month Pass
    "Frequent Flyer":       "LNK_468D3W49LB",   # 3-Month Pass
    "Full Year Experience": "LNK_253P067SB1"    # Yearly Pass
}
# ← …y con esto se actualizan todos los enlaces de pago


PREFIX = "*PNP Television on Telegram*\n\n"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ——— Estado de usuario ———
user_state = {}

# ——— Función auxiliar ———
def generate_bold_link(link_id: str, user_id: int) -> str:
    return (
        f"https://checkout.bold.co/payment/{link_id}"
        f"?identity_key={BOLD_IDENTITY_KEY}"
        f"&metadata[user_id]={user_id}"
    )

# ——— Textos y traducciones ———
TEXTS = {
    "en": {
        "welcome": "Welcome! Dive into the world of PNP Television.",
        "main_menu_plans": "Subscription Plans",
        "plans_desc": (
            "PNP Television is the ultimate interactive community for Party’n’Play lovers.\n"
            "Connect with international performers and fellow fans in live shows and private chats.\n"
            "Enjoy exclusive content, behind-the-scenes access, and VIP experiences.\n"
            "Our platform values freedom, respect, and authentic connections.\n"
            "Join us now and be part of a global family."
        ),
        "plan_menu_1": "Trial Trip - $9.99",
        "plan_menu_2": "Monthly Adventure - $14.99",
        "plan_menu_3": "Frequent Flyer - $29.99",
        "plan_menu_4": "Full Year Experience - $99.99",
        "policies_menu": "Terms, Conditions & Regulations",
        "terms_label": "Terms & Conditions",
        "privacy_label": "Privacy Policy",
        "refund_label": "Refund Policy",
        "terms_content": (
            "Terms & Conditions\n\n"
            "• You must be 18 years or older to use this service.\n"
            "• All video elements (parties, costumes, props, simulated substances) are purely artistic and not to be taken literally.\n"
            "• PNP Television does not promote substance use. If you or someone you know is struggling, please seek professional help.\n"
            "• Content is for entertainment purposes only."
        ),
        "privacy_content": (
            "Privacy Policy\n\n"
            "• We respect your privacy and will never share your data with third parties.\n"
            "• We collect only your Telegram username and usage stats to send you updates.\n"
            "• All video elements are artistic props; no real-world endorsement implied.\n"
            "• PNP Television does not condone illegal activities."
        ),
        "refund_content": (
            "Refund Policy\n\n"
            "• All purchases are final and non-refundable unless required by law.\n"
            "• No credits or refunds for canceled subscriptions.\n\n"
            "_Note:_ All video elements (props, performances, simulated substances) are for artistic effect only. PNP Television does not promote substance use and recommends seeking professional help if needed."
        ),
        "contact_label": "Contact PNP Television",
        "back": "🔙 Back"
    },
    "es": {
        "welcome": "¡Bienvenido! Sumérgete en el mundo de PNP Televisión.",
        "main_menu_plans": "Planes de suscripción",
        "plans_desc": (
            "PNP Televisión es la comunidad interactiva definitiva para amantes de Party’n’Play.\n"
            "Conéctate con performers internacionales y otros fans en shows en vivo y chats privados.\n"
            "Disfruta contenido exclusivo, acceso detrás de cámaras y experiencias VIP.\n"
            "Nuestra plataforma valora la libertad, el respeto y las conexiones auténticas.\n"
            "Únete ahora y forma parte de una familia global."
        ),
        "plan_menu_1": "Trial Trip - $9.99",
        "plan_menu_2": "Monthly Adventure - $14.99",
        "plan_menu_3": "Frequent Flyer - $29.99",
        "plan_menu_4": "Full Year Experience - $99.99",
        "policies_menu": "Términos, Condiciones y Reglamentos",
        "terms_label": "Términos y Condiciones",
        "privacy_label": "Política de Privacidad",
        "refund_label": "Política de Reembolsos",
        "terms_content": (
            "Términos y Condiciones\n\n"
            "• Debes tener 18 años o más para usar este servicio.\n"
            "• Todos los elementos de video (fiestas, disfraces, props, sustancias simuladas) son artísticos y no deben tomarse al pie de la letra.\n"
            "• PNP Televisión no promueve el uso de sustancias. Si tú o alguien que conoces lo necesita, busca ayuda profesional.\n"
            "• El contenido es solo con fines de entretenimiento."
        ),
        "privacy_content": (
            "Política de Privacidad\n\n"
            "• Respetamos tu privacidad y no compartiremos tus datos con terceros.\n"
            "• Solo recopilamos tu usuario de Telegram y estadísticas de uso para enviarte actualizaciones.\n"
            "• Todos los elementos de video son props artísticos; no implican respaldo real.\n"
            "• PNP Televisión no avala actividades ilegales."
        ),
        "refund_content": (
            "Política de Reembolsos\n\n"
            "• Todas las compras son finales y no reembolsables, salvo exigencia legal.\n"
            "• No hay créditos ni devoluciones por cancelación de suscripciones.\n\n"
            "_Nota:_ Todos los elementos de video (props, shows, sustancias simuladas) son solo artísticos. PNP Televisión no promueve el uso de sustancias y recomienda ayuda profesional si sea necesario."
        ),
        "contact_label": "Comunícate con PNP Televisión",
        "back": "🔙 Volver"
    }
}

# ——— Handlers ———

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("Español", callback_data="lang_es")]
    ]
    await update.message.reply_text(
        PREFIX + TEXTS["en"]["welcome"],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    user_state[query.from_user.id] = lang
    await show_main_menu(query, context)

async def show_main_menu(query: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = query.data.split("_")[-1]
    texts = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(texts["main_menu_plans"], callback_data=f"show_plans_{lang}")],
        [InlineKeyboardButton(texts["policies_menu"],   callback_data=f"policies_{lang}")],
        [InlineKeyboardButton(texts["contact_label"],   callback_data=f"contact_{lang}")]
    ]
    await query.edit_message_text(
        PREFIX + texts["welcome"],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def show_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Antes usábamos split("_")[1] y daba 'plans'; ahora tomamos el último elemento:
    lang = query.data.split("_")[-1]
    texts = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(texts["plan_menu_1"], callback_data=f"plan_1_{lang}")],
        [InlineKeyboardButton(texts["plan_menu_2"], callback_data=f"plan_2_{lang}")],
        [InlineKeyboardButton(texts["plan_menu_3"], callback_data=f"plan_3_{lang}")],
        [InlineKeyboardButton(texts["plan_menu_4"], callback_data=f"plan_4_{lang}")],
        [InlineKeyboardButton(texts["back"],         callback_data=f"back_to_main_{lang}")]
    ]
    await query.edit_message_text(
        PREFIX + texts["plans_desc"],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_main_menu(query, context)

async def show_plan_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, num, lang = query.data.split("_")

    # Mapa de información de cada plan
    info_map = {
        "1": {"name": "Trial Trip",           "duration": "7 days",   "price": "$9.99"},
        "2": {"name": "Monthly Adventure",    "duration": "30 days",  "price": "$14.99"},
        "3": {"name": "Frequent Flyer",       "duration": "90 days",  "price": "$29.99"},
        "4": {"name": "Full Year Experience", "duration": "365 days", "price": "$99.99"}
    }
    info = info_map[num]

    text = (
        f"*{info['name']}*\n\n"
        f"Duration: {info['duration']}\n"
        f"Price: {info['price']}\n"
        "Benefits:\n"
        " - Main PNP Television channel\n"
        " - Exclusive PNP Television group\n"
        "Bonus: Access to PNP Television Virtual Parties"
    )

    # Ahora usamos info['name'] como clave para PLAN_LINK_IDS
    link_id = PLAN_LINK_IDS[info['name']]
    kb = [
        [
            InlineKeyboardButton(
                "💳 Pagar ahora",
                url=generate_bold_link(link_id, query.from_user.id)
            )
        ],
        [
            InlineKeyboardButton(
                TEXTS[lang]["back"],
                callback_data=f"back_to_plans_{lang}"
            )
        ]
    ]

    await query.edit_message_text(
        PREFIX + text,
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

async def back_to_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_plans(update, context)

async def show_policies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    texts = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(texts["terms_label"], callback_data=f"terms_{lang}")],
        [InlineKeyboardButton(texts["privacy_label"], callback_data=f"privacy_{lang}")],
        [InlineKeyboardButton(texts["refund_label"], callback_data=f"refund_{lang}")],
        [InlineKeyboardButton(texts["back"],          callback_data=f"back_to_main_{lang}")]
    ]
    await query.edit_message_text(
        PREFIX + texts["policies_menu"],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_policy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key, lang = query.data.split("_")
    content = TEXTS[lang][f"{key}_content"]
    keyboard = [[InlineKeyboardButton(TEXTS[lang]["back"], callback_data=f"back_to_main_{lang}")]]
    await query.edit_message_text(
        PREFIX + content,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    texts = TEXTS[lang]
    keyboard = [
        [
            InlineKeyboardButton(
                texts["contact_label"],
                url="https://docs.google.com/forms/d/e/1FAIpQLSfDSj8959dxO1BeYDOjxPvQwUxWlyySG3FVkG7qx7KazERAiA/viewform?usp=header"
            )
        ],
        [InlineKeyboardButton(TEXTS[lang]["back"], callback_data=f"back_to_main_{lang}")]
    ]
    await query.edit_message_text(
        PREFIX,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def add_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    invite = await context.bot.create_chat_invite_link(chat_id=chat_id)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"🔗 Únete al canal con este enlace:\n{invite.invite_link}"
    )

async def remove_from_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    await context.bot.ban_chat_member(chat_id=chat_id, user_id=target.id)
    await context.bot.unban_chat_member(chat_id=chat_id, user_id=target.id)
    await update.message.reply_text(f"🗑️ He removido a {target.full_name} del canal.")

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        PREFIX + "👑 Welcome, Admin! What would you like to do?\n\n- /stats\n- /broadcast\n- /expire\n- etc.",
        parse_mode="Markdown"
    )

async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("admin_"):
        await context.bot.send_message(query.message.chat.id, "⚙️ Admin Panel actions here.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("entrar", add_to_channel))
    app.add_handler(CommandHandler("sacar", remove_from_channel))
    app.add_handler(CommandHandler("admin", admin_menu))

    # CallbackQueryHandlers
    app.add_handler(CallbackQueryHandler(handle_language,      pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(show_plans,           pattern="^show_plans_"))
    app.add_handler(CallbackQueryHandler(back_to_main,         pattern="^back_to_main_"))
    app.add_handler(CallbackQueryHandler(show_plan_detail,     pattern="^plan_"))
    app.add_handler(CallbackQueryHandler(back_to_plans,        pattern="^back_to_plans_"))
    app.add_handler(CallbackQueryHandler(show_policies,        pattern="^policies_"))
    app.add_handler(CallbackQueryHandler(handle_policy,        pattern="^(terms|privacy|refund)_"))
    app.add_handler(CallbackQueryHandler(handle_contact,       pattern="^contact_"))
    app.add_handler(CallbackQueryHandler(admin_callback_handler, pattern="^admin_"))

    app.run_polling()

if __name__ == "__main__":
    main()
