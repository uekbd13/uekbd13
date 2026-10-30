import os
import time
import winreg
import random
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

def human_type(element, text):
    """ دالة ذكية تكتب النص حرفاً بحرف وبسرعات متفاوتة لتبدو كإنسان وتتجنب كشف الكابتشا """
    element.click()
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) # تأخير عشوائي بين الحروف

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! استخدم الأمر /streak لبدء استعادة الستريك تلقائياً.")

async def process_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text(f"⏳ جاري فتح المتصفح ومحاكاة الكتابة البشرية لتفادي الحماية للبلد `{TARGET_FRIEND}`...", parse_mode='Markdown')
    
    driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--start-maximized")

        chrome_path = get_chrome_path_from_registry()
        options.binary_location = chrome_path
        
        driver = uc.Chrome(options=options, browser_executable_path=chrome_path)
        driver.maximize_window()

        url = "https://snapchat.com"
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        
        # الانتظار حتى يستقر الموقع تماماً
        time.sleep(6)

        # التحويل التلقائي لداخل الإطار (iframe) الخاص بالنموذج
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'ticket') or contains(@id, 'ticket')]")))
                driver.switch_to.frame(iframe)
            except:
                try: driver.switch_to.frame(0)
                except: pass

        # 1. تعبئة حقل "اسم المستخدم" بمحاكاة بشرية
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='username' or @name='username' or contains(@aria-label, 'المستخدم') or contains(@placeholder, 'حساب سناب')]")))
        human_type(username_field, MY_USERNAME)
        time.sleep(1)

        # 2. تعبئة حقل "البريد الإلكتروني" بمحاكاة بشرية
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='email' or @type='email' or contains(@aria-label, 'البريد') or contains(@name, 'email')]")))
        human_type(email_field, MY_EMAIL)
        time.sleep(1)

        # 3. تعبئة حقل "رقم الجوّال" بمحاكاة بشرية
        phone_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='phone' or @type='tel' or contains(@aria-label, 'الجوال') or contains(@name, 'phone')]")))
        human_type(phone_field, MY_PHONE)
        time.sleep(1)

        # 4. تعبئة حقل "اسم مستخدم الصديق" بمحاكاة بشرية
        try:
            friend_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'friend') or contains(@name, 'friend') or contains(@aria-label, 'صديق')]")))
        except:
            friend_field = driver.find_elements(By.XPATH, "//input[@type='text']")[-1]
            
        human_type(friend_field, TARGET_FRIEND)
        time.sleep(2)

        # 🛠️ تم إزالة الضغط التلقائي على زر الإرسال وإغلاق المتصفح لكي لا يتم حظرك من الـ reCAPTCHA
        await status_msg.edit_text(f"👋 تم تجهيز وكتابة البيانات في المتصفح بنجاح! تفضل بحل الكابتشا (إن ظهرت) واضغط إرسال في شاشتك يدوياً الآن.", parse_mode='Markdown')

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء التعبئة التلقائية.\nالتفاصيل: `{str(e)[:120]}`", parse_mode='Markdown')
        if driver is not None:
            try: driver.quit()
            except: pass

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("streak", process_streak))
    print("🤖 البوت يعمل ومستعد للتجربة اليدوية الآمنة...")
    app.run_polling()
