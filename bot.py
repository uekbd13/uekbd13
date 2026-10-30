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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! استخدم الأمر /streak لبدء استعادة الستريك تلقائياً.")

async def process_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text(f"⏳ جاري فتح صفحة الدعم والوصول للنموذج تلقائياً للصديق `{TARGET_FRIEND}`...", parse_mode='Markdown')
    
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

        # فتح الرابط الأساسي
        url = "https://help.snapchat.com/hc/ar/requests/new?co=true&ticket_form_id=149423"
        driver.get(url)
        
        wait = WebDriverWait(driver, 25)
        
        # خطوة ذكية: فحص ما إذا كان الموقع قام بالتحويل ويحتاج إلى ضغط زر "فقدت الستريك" لإظهار الحقول
        try:
            # البحث عن خيار "فقدت الستريك" أو "I lost my Snapstreak" وضغطه تلقائياً إذا ظهرت الصفحة العامة
            streak_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'ستريك') or contains(., 'Snapstreak')] | //input[@value='streak']")))
            streak_option.click()
            time.sleep(3)
        except:
            # إذا فتحت صفحة الحقول مباشرة سيتخطى الخطوة السابقة ويكمل التعبئة
            pass

        # الانتقال لداخل الـ iframe الخاص بالنموذج إن وُجد
        if len(driver.find_elements(By.TAG_NAME, "iframe")) > 0:
            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'ticket') or contains(@id, 'ticket')]")))
                driver.switch_to.frame(iframe)
            except:
                try: driver.switch_to.frame(0)
                except: pass

        # تعبئة الحقول المصححة
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'username') or contains(@name, 'username') or @type='text']")))
        username_field.clear()
        username_field.send_keys(MY_USERNAME)

        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type, 'email') or contains(@id, 'email')]")))
        email_field.clear()
        email_field.send_keys(MY_EMAIL)

        phone_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@type, 'tel') or contains(@id, 'phone')]")))
        phone_field.clear()
        phone_field.send_keys(MY_PHONE)

        friend_field = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, 'friend') or contains(@name, 'friend') or @type='text'])[last()]")))
        friend_field.clear()
        friend_field.send_keys(TARGET_FRIEND)

        time.sleep(2)

        # الضغط على زر الإرسال
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit'] | //button[@type='submit'] | //button[contains(text(), 'إرسال')]")))
        submit_btn.click()
        
        time.sleep(6)
        await status_msg.edit_text(f"✅ تم إرسال طلب الستريك للصديق `{TARGET_FRIEND}` بنجاح تام!", parse_mode='Markdown')

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
