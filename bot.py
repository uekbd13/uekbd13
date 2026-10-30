import os
import time
import winreg  # مكتبة خاصة بالويندوز لجلب مسار البرامج بدقة
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# --- البيانات الحقيقية الخاصة بك ---
BOT_TOKEN = "9098011021:AAFrQh6ShkwI3ZSMjyAXVwSncOBNjpKtIRg"
MY_USERNAME = "edk-9"
MY_EMAIL = "almqlz5854@gmail.com"
MY_PHONE = "0509334095"
TARGET_FRIEND = "em_ad311"

def get_chrome_path_from_registry():
    """ جلب مسار متصفح كروم الحقيقي المثبت في نظام الويندوز الخاص بك """
    try:
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
            return winreg.QueryValue(key, None)
    except:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                return winreg.QueryValue(key, None)
        except:
            return r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! استخدم الأمر /streak لبدء استعادة الستريك تلقائياً.")

async def process_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text(f"⏳ جاري محاولة إرسال طلب استعادة الستريك للصديق `{TARGET_FRIEND}`...", parse_mode='Markdown')
    
    driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        # جلب المسار الفعلي لكروم من جهازك وتمريره برمجياً
        chrome_path = get_chrome_path_from_registry()
        options.binary_location = chrome_path
        
        driver = uc.Chrome(options=options, browser_executable_path=chrome_path)

        url = "https://snapchat.com"
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'username') or contains(@name, 'username') or contains(@placeholder, 'اسم المستخدم')]")))
        username_field.send_keys(MY_USERNAME)

        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type, 'email') or contains(@id, 'email') or contains(@name, 'email')]")))
        email_field.send_keys(MY_EMAIL)

        phone_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type, 'tel') or contains(@id, 'phone') or contains(@name, 'phone') or contains(@placeholder, 'الهاتف')]")))
        phone_field.send_keys(MY_PHONE)

        friend_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'friend') or contains(@name, 'friend') or contains(@placeholder, 'الصديق')]")))
        friend_field.send_keys(TARGET_FRIEND)

        time.sleep(2)

        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'] | //button[@type='submit'] | //input[contains(@value, 'إرسال')] | //button[contains(text(), 'إرسال')]")))
        submit_btn.click()
        
        time.sleep(5)
        
        await status_msg.edit_text(f"✅ تم إرسال طلب الستريك للصديق `{TARGET_FRIEND}` بنجاح تام!", parse_mode='Markdown')

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء التعبئة التلقائية.\nالتفاصيل: `{str(e)[:150]}`", parse_mode='Markdown')
    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("streak", process_streak))
    print("🤖 البوت يعمل على الـ CMD بنجاح...")
    app.run_polling()
