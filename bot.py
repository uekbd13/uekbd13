import os
import time
import platform
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# --- البيانات الحقيقية الكاملة والمصححة ---
BOT_TOKEN = "9098011021:AAFrQh6ShkwI3ZSMjyAXVwSncOBNjpKtIRg"
MY_USERNAME = "edk-9"
MY_EMAIL = "almqlz5854@gmail.com"
MY_PHONE = "0509334095"
TARGET_FRIEND = "em_ad311"

def find_chrome_path():
    """ دالة ذكية للبحث التلقائي عن مسار كروم في الويندوز لتجنب خطأ عدم العثور عليه """
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Google\Chrome SxS\Application\chrome.exe" # Chrome Canary
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

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

        current_os = platform.system().lower()
        
        if "windows" in current_os:
            chrome_path = find_chrome_path()
            if chrome_path:
                options.binary_location = chrome_path
                driver = uc.Chrome(options=options, browser_executable_path=chrome_path)
            else:
                # إذا لم يجد مسار كروم العادي، يحاول التشغيل بدون تحديد المسار كخيار أخير
                driver = uc.Chrome(options=options)
        else:
            chrome_bin = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")
            options.binary_location = chrome_bin
            driver = uc.Chrome(options=options)

        url = "https://snapchat.com"
        driver.get(url)
        
        wait = WebDriverWait(driver, 20)
        
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'username') or contains(@name, 'username')]")))
        username_field.send_keys(MY_USERNAME)

        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type, 'email') or contains(@id, 'email')]")))
        email_field.send_keys(MY_EMAIL)

        phone_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type, 'tel') or contains(@id, 'phone')]")))
        phone_field.send_keys(MY_PHONE)

        friend_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'friend') or contains(@name, 'friend')]")))
        friend_field.send_keys(TARGET_FRIEND)

        time.sleep(2)

        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'] | //button[@type='submit']")))
        submit_btn.click()
        
        time.sleep(5)
        
        await status_msg.edit_text(f"✅ تم إرسال طلب الستريك للصديق `{TARGET_FRIEND}` بنجاح تام!", parse_mode='Markdown')

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء التعبئة التلقائية.\nالتفاصيل: `{str(e)}`", parse_mode='Markdown')
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
    print("🤖 البوت يعمل...")
    app.run_polling()
