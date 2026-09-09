import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# الروابط الرئيسية
WHATSAPP_LINK = "https://wa.me/201224519695"
WEBSITE_LINK = "https://mamdouhhassan.vercel.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # قائمة الأزرار التفاعلية الشاملة
    keyboard = [
        [InlineKeyboardButton("📖 | تصفح صور الأعمال", callback_data='view_portfolio')],
        [InlineKeyboardButton("📚 | تحميل عينات كتب (PDF)", callback_data='view_pdf_samples')],
        [InlineKeyboardButton("🌐 | زيارة الموقع الإلكتروني", url=WEBSITE_LINK)],
        [
            InlineKeyboardButton("✉️ | إرسال استفسار", callback_data='contact'),
            InlineKeyboardButton("💬 | تواصل عبر واتساب", url=WHATSAPP_LINK)
        ],
        [InlineKeyboardButton("📄 | السيرة الذاتية (CV)", callback_data='cv')]
    ]
    
    welcome_text = (
        "✨ مرحباً بكم في عالم الإخراج المكتبي ✨\n\n"
        "👤 أنا المساعد الشخصي للأستاذ ممدوح حسن\n"
        "📖 خبير تنسيق وإخراج الكتب والمخطوطات والرصف المكتبي.\n\n"
        "👇 الرجاء اختيار الخدمة المطلوبة من الأزرار أدناه:"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 1. معرض صور الأعمال
    if query.data == 'view_portfolio':
        media_group = [
            InputMediaPhoto(f"{WEBSITE_LINK}/sample1.jpg", caption="📖 نموذج إخراج كتاب أدبي وتنسيق الصفحات"),
            InputMediaPhoto(f"{WEBSITE_LINK}/sample2.jpg", caption="📜 نموذج تنسيق قصيدة شعرية وعمودين"),
            InputMediaPhoto(f"{WEBSITE_LINK}/sample3.jpg", caption="✨ نموذج تنسيق هوامش ومخطوطات")
        ]
        await context.bot.send_media_group(chat_id=query.message.chat_id, media=media_group)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"هذه عينة سريعة من أحدث الأعمال! لمشاهدة التفاصيل وتصفح الحزم الكاملة تفضل بزيارة موقعنا:\n{WEBSITE_LINK}"
        )

    # 2. ملفات الـ PDF المباشرة
    elif query.data == 'view_pdf_samples':
        await context.bot.send_message(chat_id=query.message.chat_id, text="جاري تحميل وإرسال عينات الكتب بصيغة PDF... ⏳")
        
        # إرسال العينة الأولى
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=f"{WEBSITE_LINK}/sample1.pdf",
            filename="عينة_تنسيق_كتاب1.pdf",
            caption="📄 عينة تنسيق كتاب أدبي (PDF)"
        )
        
        # إرسال العينة الثانية
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=f"{WEBSITE_LINK}/sample2.pdf",
            filename="عينة_تنسيق_كتاب2.pdf",
            caption="📄 عينة تنسيق ديوان شعر / كتاب (PDF)"
        )

    # 3. إرسال استفسار
    elif query.data == 'contact':
        await query.message.reply_text(
            f"📨 تفضل بكتابة استفسارك أو تفاصيل مشروعك هنا وسيتم الرد عليك في أقرب وقت.\n\n"
            f"أو يمكنك التواصل المباشر والسريع عبر الواتساب:\n{WHATSAPP_LINK}"
        )

    # 4. السيرة الذاتية
    elif query.data == 'cv':
        await query.message.reply_text(
            "📄 **الأستاذ ممدوح حسن**\n\n"
            "• خبير تنسيق ورصف الكتب وإخراج المخطوطات والقصائد الشعرية بخبرة تتجاوز 25 عاماً.\n"
            "• متخصص في ضبط خطوط اللوتس والأميري وإخراج الجداول والدراسات الأكاديمية.\n"
            "• مطور أدوات وماكروهات أتمتة تنسيق النصوص ببرنامج Microsoft Word و Python."
        )

if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))
    print("Bot is running... @MamdouhPortfolio_bot")
    application.run_polling()