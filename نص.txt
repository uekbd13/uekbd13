import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

MY_USERNAME = "edk-9"
MY_EMAIL = "almqlz5854@gmail.com"
MY_PHONE = "0509334095"
TARGET_FRIEND = "em_ad311"
BOT_TOKEN = "9098011021:AAGOS_yi0UB6V-psUR4aAcoKmdB-9oOoJ-c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك! البوت جاهز الآن.\n\n"
        "فقط أرسل الأمر:\n`/streak`\n\n"
        "وسيقوم بإرسال الطلب لصديقك `em_ad311` تلقائياً!",
        parse_mode='Markdown'
    )

async def process_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text(f"⏳ جاري إرسال طلب استعادة الستريك للصديق `{TARGET_FRIEND}`...", parse_mode='Markdown')

    try:
        options = Options()
        options.add_argument("-headless")
        
        driver = webdriver.Firefox(options=options)
        url = "https://help.snapchat.com/hc/ar/requests/new?co=true&ticket_form_id=149423"
        driver.get(url)
        time.sleep(4)

        inputs = driver.find_elements(By.TAG_NAME, "input")
        for i in inputs:
            name_attr = (i.get_attribute("name") or "").lower()
            if "username" in name_attr and not i.get_attribute("value"):
                i.send_keys(MY_USERNAME)
            elif "email" in name_attr:
                i.send_keys(MY_EMAIL)
            elif "phone" in name_attr:
                i.send_keys(MY_PHONE)

        all_fields = driver.find_elements(By.TAG_NAME, "input") + driver.find_elements(By.TAG_NAME, "textarea")
        for field in all_fields:
            name_attr = (field.get_attribute("name") or "").lower()
            id_attr = (field.get_attribute("id") or "").lower()
            if "friend" in name_attr or "friend" in id_attr or "description" in name_attr:
                field.send_keys(TARGET_FRIEND)

        time.sleep(2)

        buttons = driver.find_elements(By.TAG_NAME, "button") + driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
        submitted = False
        for btn in buttons:
            btn_text = btn.text.lower() if btn.text else ""
            if "إرسال" in btn_text or "submit" in btn_text or "send" in btn_text:
                btn.click()
                submitted = True
                break

        driver.quit()

        if submitted:
            await status_msg.edit_text(f"✅ تم إرسال طلب الستريك للصديق `{TARGET_FRIEND}` بنجاح تام!", parse_mode='Markdown')
        else:
            await status_msg.edit_text(f"⚠️ تم تعبئة البيانات للصديق `{TARGET_FRIEND}`، راجع حالة الطلب.", parse_mode='Markdown')

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("streak", process_streak))
    
    print("🤖 البوت يعمل...")
    app.run_polling()
