#!/usr/bin/env python3
"""
Twitter Login Debug Script
Login sürecini adım adım gösterir ve screenshot alır.
"""

import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

async def debug_login():
    """Twitter login'i debug et"""

    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')
    email = os.getenv('TWITTER_EMAIL')

    print(f"🔐 Kullanıcı: {username}")
    print(f"📧 Email: {email}")
    print(f"🔑 Şifre: {'*' * len(password)}\n")

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled'],
        slow_mo=1000  # Her işlem arası 1 saniye bekle (görmek için)
    )

    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    page = await context.new_page()

    try:
        # 1. Login sayfasına git
        print("1️⃣ Login sayfasına gidiliyor...")
        await page.goto('https://twitter.com/i/flow/login', timeout=60000)
        await asyncio.sleep(3)
        await page.screenshot(path='debug_1_login_page.png')
        print("   ✅ Screenshot: debug_1_login_page.png")

        # 2. Username input'unu bul ve doldur
        print("\n2️⃣ Username giriliyor...")
        try:
            username_input = await page.wait_for_selector('input[autocomplete="username"]', timeout=20000)
            await username_input.fill(username)
            await asyncio.sleep(1)
            await page.screenshot(path='debug_2_username_filled.png')
            print("   ✅ Username girildi")
            print("   ✅ Screenshot: debug_2_username_filled.png")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            await page.screenshot(path='debug_2_error.png')
            raise

        # 3. Next butonuna tıkla
        print("\n3️⃣ Next butonuna tıklanıyor...")
        try:
            # Önce "İleri" veya "Next" text'ini içeren span'ı bul
            await asyncio.sleep(1)

            # Yöntem 1: Text içeriğine göre ara
            ileri_button = await page.get_by_text('İleri').first
            if ileri_button:
                await ileri_button.click()
                print("   ✅ 'İleri' butonuna tıklandı")
            else:
                # Yöntem 2: Manuel selector
                await page.click('button:has-text("İleri")')
                print("   ✅ Butona tıklandı (alternatif yöntem)")

            await asyncio.sleep(4)
            await page.screenshot(path='debug_3_after_next.png')
            print("   ✅ Screenshot: debug_3_after_next.png")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            print("   ℹ️ Enter tuşu ile deneniyor...")
            await page.keyboard.press('Enter')
            await asyncio.sleep(3)
            await page.screenshot(path='debug_3_error.png')

        # 4. Email kontrolü (bazen sorar)
        print("\n4️⃣ Email kontrolü...")
        try:
            email_input = await page.wait_for_selector('input[data-testid="ocfEnterTextTextInput"]', timeout=5000)
            print("   ⚠️ Email/telefon doğrulama isteniyor!")
            if email_input and email:
                await email_input.fill(email)
                await asyncio.sleep(1)
                await page.screenshot(path='debug_4_email_filled.png')
                print(f"   ✅ Email girildi: {email}")

                # Next butonuna tekrar tıkla
                try:
                    await page.click('button:has-text("İleri")')
                    print("   ✅ 'İleri' butonuna tıklandı")
                except:
                    await page.keyboard.press('Enter')
                    print("   ✅ Enter tuşuna basıldı")
                await asyncio.sleep(3)
                await page.screenshot(path='debug_4_after_email.png')
        except Exception as e:
            print("   ℹ️ Email istenmedi (normal)")
            await page.screenshot(path='debug_4_no_email.png')

        # 5. Password input'unu bul ve doldur
        print("\n5️⃣ Password giriliyor...")
        try:
            password_input = await page.wait_for_selector('input[name="password"]', timeout=20000)
            await password_input.fill(password)
            await asyncio.sleep(1)
            await page.screenshot(path='debug_5_password_filled.png')
            print("   ✅ Password girildi")
            print("   ✅ Screenshot: debug_5_password_filled.png")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            await page.screenshot(path='debug_5_error.png')
            print("   📋 Sayfa HTML'i:")
            print(await page.content())
            raise

        # 6. Login butonuna tıkla
        print("\n6️⃣ Login butonuna tıklanıyor...")
        try:
            # "Giriş yap" veya "Log in" butonunu bul
            try:
                await page.click('button:has-text("Giriş yap")')
                print("   ✅ 'Giriş yap' butonuna tıklandı")
            except:
                try:
                    await page.click('button:has-text("Log in")')
                    print("   ✅ 'Log in' butonuna tıklandı")
                except:
                    # Son çare: Enter tuşu
                    await page.keyboard.press('Enter')
                    print("   ✅ Enter tuşuna basıldı")
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            await page.screenshot(path='debug_6_error.png')
            raise

        # 7. Login sonrası bekle
        print("\n7️⃣ Login sonucu bekleniyor...")
        await asyncio.sleep(10)

        current_url = page.url
        await page.screenshot(path='debug_7_final.png')

        print(f"\n📍 Son URL: {current_url}")
        print("   ✅ Screenshot: debug_7_final.png")

        # Login başarılı mı kontrol et
        if 'home' in current_url.lower():
            print("\n✅ ✅ ✅ LOGIN BAŞARILI! ✅ ✅ ✅")
            return True
        else:
            print(f"\n❌ Login başarısız! URL: {current_url}")

            # Hata mesajı var mı kontrol et
            try:
                error_text = await page.query_selector('span[data-testid="error-detail"]')
                if error_text:
                    error_msg = await error_text.inner_text()
                    print(f"   ⚠️ Hata mesajı: {error_msg}")
            except:
                pass

            print("\n⏳ 30 saniye bekliyorum - manuel olarak bir şey yapmanız gerekiyorsa yapın...")
            await asyncio.sleep(30)

            await page.screenshot(path='debug_8_after_wait.png')
            final_url = page.url
            print(f"\n📍 30 saniye sonra URL: {final_url}")

            if 'home' in final_url.lower():
                print("\n✅ LOGIN BAŞARILI (manuel düzeltme sonrası)!")
                return True

            return False

    except Exception as e:
        print(f"\n💥 HATA: {e}")
        await page.screenshot(path='debug_error_final.png')
        return False
    finally:
        print("\n🖼️ Tüm screenshot'lar kaydedildi!")
        print("📂 Dosyalar: twitter-telegram-bot/ klasöründe")
        print("\n⏸️ Browser açık kalacak - incelemek için 60 saniye bekliyorum...")
        await asyncio.sleep(60)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_login())
