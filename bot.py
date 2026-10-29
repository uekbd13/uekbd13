import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 

MY_USERNAME = "edk-9"
MY_EMAIL = "almqlz5854@gmail.com"
MY_PHONE = "0509334095"
TARGET_FRIEND = "em_ad311"
BOT_TOKEN = "9098011021:AAFrQh6ShkwI3ZSMjyAXVwSncOBNjpKtIRg"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك! البوت جاهز الآن.\n\n"
        "فقط أرسل الأمر:\n`/streak`\n\n"
        "وسيقوم بإرسال الطلب تلقائياً!",
        parse_mode='Markdown'
    )

async def process_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text(f"⏳ جاري محاولة إرسال طلب استعادة الستريك للصديق `{TARGET_FRIEND}`...", parse_mode='Markdown')

    try:
          # إعداد المتصفح ليتوافق مع جهازك
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')  # التشغيل في الخلفية
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        # تحديد مسار متصفح كروم في الويندوز
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
        # تشغيل المتصفح بالمسار المحدد
        driver = uc.Chrome(options=options, browser_executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")

        # جلب مسار متصفح كروم من متغيرات البيئة التي أضفتها في Render
        chrome_bin = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")
        options.binary_location = chrome_bin
        
        # تشغيل المتصفح
        driver = uc.Chrome(options=options)
        url = "https://help.snapchat.com/hc/ar/requests/new?co=true&ticket_form_id=149423"
        driver.get(url)
        
        # انتظر تحميل العناصر الأساسية (أقصى مدة 15 ثانية)
        wait = WebDriverWait(driver, 15)
        
        # انتظر وتأكد من وجود الحقول واكتب داخلها عبر Xpath
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'username') or contains(@name, 'username')]")))
        username_field.send_keys(MY_USERNAME)

        email_field = driver.find_element(By.XPATH, "//input[contains(@type, 'email') or contains(@id, 'email')]")
        email_field.send_keys(MY_EMAIL)

        phone_field = driver.find_element(By.XPATH, "//input[contains(@type, 'tel') or contains(@id, 'phone')]")
        phone_field.send_keys(MY_PHONE)

        # حقل اسم المستخدم للصديق
        friend_field = driver.find_element(By.XPATH, "//input[contains(@id, 'friend') or contains(@name, 'friend')]")
        friend_field.send_keys(TARGET_FRIEND)

        time.sleep(2)

        # الضغط على زر الإرسال
        submit_btn = driver.find_element(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
        submit_btn.click()
        
        time.sleep(5) # انتظار معالجة الطلب
        
        driver.quit()
        await status_msg.edit_text(f"✅ تم إرسال طلب الستريك للصديق `{TARGET_FRIEND}` بنجاح تام!", parse_mode='Markdown')

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        await status_msg.edit_text(f"❌ حدث خطأ أثناء التعبئة التلقائية.\nالسبب المحتمل: ظهور اختبار الكابتشا (CAPTCHA) أو تغير تصميم حقول الموقع.\nالتفاصيل: `{str(e)}`", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("streak", process_streak))
    
    print("🤖 البوت يعمل...")
    app.run_polling()
