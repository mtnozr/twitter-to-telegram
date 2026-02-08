#!/usr/bin/env python3
"""Twitter hesabını twscrape'e ekle"""
import asyncio
from twscrape import API
import os
from dotenv import load_dotenv

load_dotenv()

async def setup():
    api = API()

    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')
    email = os.getenv('TWITTER_EMAIL')

    print(f"Hesap ekleniyor: {username}")

    # Hesabı ekle
    await api.pool.add_account(username, password, email, password)

    print("Hesap eklendi! Login yapılıyor...")

    # Login yap
    await api.pool.login_all()

    print("✅ Login başarılı!")

    # Hesap durumunu kontrol et
    accounts = await api.pool.accounts_info()
    for acc in accounts:
        print(f"Hesap: {acc['username']}, Durum: {acc['status']}")

if __name__ == "__main__":
    asyncio.run(setup())
