#!/usr/bin/env python3
"""
Twitter Cookie Saver
Manuel olarak login olun, cookie'ler otomatik kaydedilecek.
"""

import asyncio
import json
from playwright.async_api import async_playwright

async def save_cookies():
    """Manuel login yapıp cookie'leri kaydet"""

    print("=" * 60)
    print("🍪 TWITTER COOKIE KAYDETME")
    print("=" * 60)
    print()
    print("📋 ADIMLAR:")
    print("1. Chrome penceresi açılacak")
    print("2. Twitter'a GİDİN ve MANUEL OLARAK login olun")
    print("3. Ana sayfaya (Home) geldiğinizde bu terminale dönün")
    print("4. 'TAMAM' yazıp Enter'a basın")
    print()
    print("🚀 Başlıyoruz...")
    print()

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )

    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    page = await context.new_page()

    # Twitter ana sayfasına git
    print("📱 Twitter açılıyor...")
    await page.goto('https://twitter.com')
    await asyncio.sleep(2)

    print()
    print("✋ ŞİMDİ SİZ DEVREYE GİRİN!")
    print()
    print("   1️⃣ Açılan Chrome penceresinde Twitter'a login olun")
    print("   2️⃣ Ana sayfaya (Home/For You) geldiğinizde")
    print("   3️⃣ Bu terminale 'TAMAM' yazıp Enter'a basın")
    print()

    # Kullanıcı login olana kadar bekle
    while True:
        user_input = input(">>> Login oldunuz mu? (TAMAM yazın): ").strip().upper()
        if user_input == "TAMAM":
            break
        elif user_input == "HAYIR" or user_input == "İPTAL":
            print("❌ İptal edildi.")
            await browser.close()
            return False
        else:
            print("   ℹ️ Lütfen 'TAMAM' yazın veya 'İPTAL' yazın")

    print()
    print("💾 Cookie'ler kaydediliyor...")

    # Cookie'leri al ve kaydet
    cookies = await context.cookies()

    with open('twitter_cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)

    print(f"✅ {len(cookies)} cookie kaydedildi!")
    print("📁 Dosya: twitter_cookies.json")
    print()

    # Test: Login kontrolü
    current_url = page.url
    page_title = await page.title()

    print("🔍 Login kontrolü:")
    print(f"   URL: {current_url}")
    print(f"   Sayfa: {page_title}")

    if 'home' in current_url.lower() or 'x.com' in current_url:
        print()
        print("✅ ✅ ✅ LOGIN BAŞARILI! ✅ ✅ ✅")
        print()
        print("🎉 Cookie'ler kaydedildi!")
        print("🚀 Artık bot.py'yi çalıştırabilirsiniz!")
        success = True
    else:
        print()
        print("⚠️ Login kontrolü başarısız!")
        print("   Lütfen Twitter'da login olduğunuzdan emin olun.")
        success = False

    await browser.close()
    return success

if __name__ == "__main__":
    result = asyncio.run(save_cookies())
    if not result:
        print("\n❌ Cookie kaydetme başarısız!")
    else:
        print("\n✅ Hazırsınız! Şimdi 'python bot.py' çalıştırın")
