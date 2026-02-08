# Twitter-Telegram Bot - PythonAnywhere Version

Bu klasör, PythonAnywhere'de 7/24 çalışacak şekilde optimize edilmiş bot versiyonunu içerir.

## 🔄 Orijinal Versiyondan Farklar

| Özellik | Orijinal (MacBook) | PythonAnywhere |
|---------|-------------------|----------------|
| **Browser** | Playwright (Chromium) | - |
| **Scraping** | Playwright | snscrape |
| **Login** | Twitter cookie'leri | Gerekli değil |
| **Bağımlılıklar** | playwright, requests | snscrape, requests |
| **Kurulum** | Playwright install | pip install |

## 📁 Dosyalar

- `bot.py` - Ana bot kodu (snscrape ile)
- `telegram_commands.py` - Telegram komut handler
- `requirements.txt` - Python bağımlılıkları
- `pythonanywhere_setup.sh` - Kurulum scripti
- `start_pythonanywhere.sh` - Başlatma scripti
- `PYTHONANYWHERE_DEPLOY.md` - Detaylı deployment rehberi
- `.env.example` - Environment variables şablonu

## 🚀 Hızlı Başlangıç

1. **PYTHONANYWHERE_DEPLOY.md** dosyasını okuyun
2. PythonAnywhere hesabı oluşturun
3. Bu klasörü PythonAnywhere'e yükleyin
4. Kurulum scriptini çalıştırın
5. .env dosyasını yapılandırın
6. Botu başlatın

## ⚠️ Önemli Notlar

- Bu versiyon **MacBook'taki orijinal botu etkilemez**
- Orijinal bot Playwright ile çalışmaya devam eder
- PythonAnywhere versiyonu snscrape kullanır
- Her iki bot da aynı anda çalışabilir (farklı anahtar kelimelerle)

## 📖 Dokümantasyon

Detaylı kurulum ve kullanım için:
👉 **[PYTHONANYWHERE_DEPLOY.md](PYTHONANYWHERE_DEPLOY.md)**

## 💡 Destek

Sorun yaşıyorsanız deployment rehberindeki "Sorun Giderme" bölümüne bakın.
