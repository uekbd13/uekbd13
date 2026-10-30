import os
import time
import winreg
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
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            return winreg.QueryValue(key, None)
    except Exception:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
                return winreg.QueryValue(key, None)
        except Exception:
            return r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! استخدم الأمر /streak لبدء استعادة الستريك تلقائياً.")

async def process_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text(f"⏳ جاري تعبئة طلب الستريك للصديق `{TARGET_FRIEND}` الحقول ظهرت في المتصفح...", parse_mode='Markdown')
    
    driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--start-maximized")

        chrome_path = get_chrome_path_from_registry()
        if chrome_path and os.path.exists(chrome_path):
            options.binary_location = chrome_path
        
        driver = uc.Chrome(options=options)
        driver.maximize_window()

        # تم تعديل الرابط ليوجه مباشرة لصفحة الدعم الخاصة بسناب شات (أو صفحة استعادة الستريك)
        url = "https://support.snapchat.com/a/lost-streak"
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        
        # الانتظار حتى استقرار الصفحة تماماً
        time.sleep(5)

        # التحويل التلقائي لداخل الإطار (iframe) الخاص بالنموذج إذا كان معزولاً
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'ticket') or contains(@id, 'ticket')]")))
                driver.switch_to.frame(iframe)
            except:
                try:
                    driver.switch_to.frame(0)
                except:
                    pass

        # 1. تعبئة حقل "اسم المستخدم"
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='username' or @name='username' or contains(@aria-label, 'المستخدم') or contains(@placeholder, 'حساب سناب')]")))
        username_field.click()
        username_field.clear()
        username_field.send_keys(MY_USERNAME)
        time.sleep(1)

        # 2. تعبئة حقل "البريد الإلكتروني"
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='email' or @type='email' or contains(@aria-label, 'البريد') or contains(@name, 'email')]")))
        email_field.click()
        email_field.clear()
        email_field.send_keys(MY_EMAIL)
        time.sleep(1)

        # 3. تعبئة حقل "رقم الجوّال"
        phone_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='phone' or @type='tel' or contains(@aria-label, 'الجوال') or contains(@name, 'phone')]")))
        phone_field.click()
        phone_field.clear()
        phone_field.send_keys(MY_PHONE)
        time.sleep(1)

        # 4. تعبئة حقل "اسم مستخدم الصديق"
        try:
            friend_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'friend') or contains(@name, 'friend') or contains(@aria-label, 'صديق')]")))
        except:
            friend_field = driver.find_elements(By.XPATH, "//input[@type='text']")[-1]
            
        friend_field.click()
        friend_field.clear()
        friend_field.send_keys(TARGET_FRIEND)
        time.sleep(1)

        # 5. الضغط على زر الإرسال
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'] | //button[@type='submit'] | //button[contains(text(), 'إرسال')]")))
        submit_btn.click()
        
        time.sleep(5)
        await status_msg.edit_text(f"✅ تم تعبئة وإرسال طلب الستريك للصديق `{TARGET_FRIEND}` بنجاح تام!", parse_mode='Markdown')

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء التعبئة التلقائية.\nالتفاصيل: `{str(e)[:120]}`", parse_mode='Markdown')
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
    print("🤖 البوت يعمل ومستعد للتجربة الآن...")
    app.run_polling()
