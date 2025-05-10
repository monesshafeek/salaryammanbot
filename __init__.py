from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# دالة بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عمك الشيخ مؤنس بحسب، أدخل القراءتين (القديمة والجديدة) بينهما سطر جديد.")

# دالة الحساب
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # نقبل التنسيقات: سطر جديد أو فاصلة أو نقطتين
    if '\n' in text:
        parts = text.split('\n')
    elif ':' in text:
        parts = text.split(':')
    elif ',' in text:
        parts = text.split(',')
    else:
        await update.message.reply_text("من فضلك، أدخل القراءتين مفصولتين بسطر جديد أو فاصلة أو نقطتين.")
        return

    if len(parts) != 2:
        await update.message.reply_text("يرجى إدخال قراءتين فقط.")
        return

    try:
        old_reading = float(parts[0].strip())
        new_reading = float(parts[1].strip())
    except ValueError:
        await update.message.reply_text("تأكد أن القراءتين أرقام صحيحة.")
        return

    if new_reading < old_reading:
        await update.message.reply_text("القراءة الجديدة يجب أن تكون أكبر من القديمة.")
        return

    consumption = new_reading - old_reading
    cost = 0

    if consumption <= 300:
        cost = consumption * 0.05
    elif consumption <= 600:
        cost = 300 * 0.05 + (consumption - 300) * 0.1
    else:
        cost = 300 * 0.05 + 300 * 0.1 + (consumption - 600) * 0.2

    message = (
        f"الاستهلاك: {consumption} كيلو وات\n"
        f"التكلفة حسب الشرائح: {cost:.3f} دينار\n"
        f"🔺 لا تنسَ إضافة الرسوم الشهرية يدويًا إلى هذا المبلغ."
    )
    await update.message.reply_text(message)

# الدالة الرئيسية لتشغيل البوت
def main():
    token = "7910706397:AAEga4tL6jgU7Rt2HEmi8EP0i44ivxulED4"  # التوكن الخاص بك
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    print("البوت يعمل الآن... جاهز لاستقبال الأوامر")
    app.run_polling()

if __name__ == "__main__":
    main()
