# PythonAnywhere Deployment Rehberi 🚀

Twitter-Telegram botunuzu PythonAnywhere'e deploy ederek 7/24 çalışmasını sağlama rehberi.

## 📋 Önemli Bilgiler

> **Not:** Bu versiyon **snscrape** kullanır (Playwright yerine)
> - ✅ Login gerektirmez
> - ✅ PythonAnywhere'de çalışır
> - ✅ Daha hafif ve hızlı
> - ⚠️ Twitter API değil, scraping kullanır

## 🎯 Adım Adım Kurulum

### 1️⃣ PythonAnywhere Hesabı Oluşturun

1. https://www.pythonanywhere.com adresine gidin
2. **"Start running Python online in less than a minute!"** butonuna tıklayın
3. Ücretsiz hesap oluşturun (Beginner account)
4. Email doğrulaması yapın

### 2️⃣ Kodu PythonAnywhere'e Yükleyin

#### Seçenek A: GitHub Üzerinden (Önerilen)

**MacBook'ta:**
```bash
cd ~/twitter-telegram-bot-pythonanywhere

# Git repository oluştur
git init
git add .
git commit -m "PythonAnywhere deployment version"

# GitHub'a push et (önce GitHub'da repo oluşturun)
git remote add origin https://github.com/KULLANICI_ADINIZ/twitter-telegram-bot.git
git push -u origin main
```

**PythonAnywhere'de:**
1. Dashboard → **"Consoles"** sekmesine gidin
2. **"Bash"** console başlatın
3. Şu komutu çalıştırın:
```bash
git clone https://github.com/KULLANICI_ADINIZ/twitter-telegram-bot.git
cd twitter-telegram-bot
```

#### Seçenek B: Manuel Upload

1. PythonAnywhere Dashboard → **"Files"** sekmesi
2. **"Upload a file"** ile dosyaları tek tek yükleyin
3. Veya zip olarak yükleyip açın:
```bash
unzip twitter-telegram-bot.zip
cd twitter-telegram-bot
```

### 3️⃣ Kurulumu Yapın

PythonAnywhere Bash console'da:

```bash
cd twitter-telegram-bot

# Kurulum scriptini çalıştır
bash pythonanywhere_setup.sh
```

Bu script:
- ✅ Virtual environment oluşturur
- ✅ Bağımlılıkları yükler (snscrape, requests, python-dotenv)
- ✅ Gerekli klasörleri hazırlar

### 4️⃣ .env Dosyasını Yapılandırın

```bash
# .env dosyasını düzenle
nano .env
```

Şu bilgileri girin:

```env
# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Search Configuration
SEARCH_KEYWORDS=bitcoin,ethereum,AI
CHECK_INTERVAL=120
MAX_TWEETS=10
TWEET_LANGUAGE=all

# Sessiz Saatler (opsiyonel)
SILENT_START=23:00
SILENT_END=08:00
```

**Kaydetmek için:** `Ctrl+O` → Enter → `Ctrl+X`

### 5️⃣ Botu Test Edin

```bash
# Virtual environment'ı aktifleştir
source venv/bin/activate

# Botu test et
python bot.py
```

Telegram'dan bildirim gelirse ✅ çalışıyor demektir!

Test ettikten sonra `Ctrl+C` ile durdurun.

### 6️⃣ Always-On Task Olarak Ayarlayın

#### Ücretsiz Plan (Workaround)

Ücretsiz planda "Always-on task" yok, ama **Scheduled Task** ile çözüm:

1. Dashboard → **"Tasks"** sekmesi
2. **"Scheduled tasks"** bölümüne gidin
3. Yeni task ekleyin:
   - **Command:** `/home/KULLANICI_ADINIZ/twitter-telegram-bot/start_pythonanywhere.sh`
   - **Hour:** Her saat için `*` veya belirli saatler
   - **Minute:** `*/5` (her 5 dakikada bir)

Bu yöntemle bot her 5 dakikada restart olur ama çalışmaya devam eder.

#### Hacker Plan ($5/ay) - Önerilen

1. Dashboard → **"Tasks"** sekmesi
2. **"Always-on tasks"** bölümüne gidin
3. Yeni task ekleyin:
   - **Command:** `/home/KULLANICI_ADINIZ/twitter-telegram-bot/start_pythonanywhere.sh`
4. **Enable** butonuna tıklayın

✅ Bot artık 7/24 kesintisiz çalışacak!

## 🔧 Yönetim Komutları

### Botu Manuel Başlatma

```bash
cd ~/twitter-telegram-bot
bash start_pythonanywhere.sh
```

### Botu Durdurma

```bash
kill $(cat ~/twitter-telegram-bot/bot.pid)
```

### Log Takibi

```bash
tail -f ~/twitter-telegram-bot/bot.log
```

### Durum Kontrolü

```bash
ps aux | grep bot.py
```

## 📱 Telegram Komutları

Bot çalışırken Telegram'dan şu komutları kullanabilirsiniz:

- `/start` - Bot bilgilerini göster
- `/help` - Yardım menüsü
- `/durum` - Bot durumunu kontrol et
- `/durdur` - Tweet takibini durdur
- `/basla` - Tweet takibini başlat
- `/kelimeler` - Anahtar kelimeleri göster

## 🐛 Sorun Giderme

### "ModuleNotFoundError: No module named 'snscrape'"

```bash
source venv/bin/activate
pip install snscrape
```

### "Permission denied" Hatası

```bash
chmod +x pythonanywhere_setup.sh
chmod +x start_pythonanywhere.sh
```

### Bot Çalışmıyor

1. Log dosyasını kontrol edin:
```bash
tail -n 50 ~/twitter-telegram-bot/bot.log
```

2. .env dosyasını kontrol edin:
```bash
cat ~/twitter-telegram-bot/.env
```

3. Process'i kontrol edin:
```bash
ps aux | grep bot.py
```

### Telegram Mesaj Gelmiyor

1. Bot token'ınızı kontrol edin
2. Chat ID'nizi kontrol edin
3. Botunuzla en az bir kez sohbet başlattığınızdan emin olun

## 💰 Maliyet Karşılaştırması

| Plan | Ücret | Always-On | CPU Time | Özellikler |
|------|-------|-----------|----------|------------|
| **Beginner** | Ücretsiz | ❌ | 100 sn/gün | Scheduled task ile workaround |
| **Hacker** | $5/ay | ✅ | Sınırsız | 7/24 kesintisiz çalışma |

**Önerim:** Hacker plan ($5/ay) - 7/24 güvenilir çalışma için

## 🔄 Güncelleme

Kodu güncellemek için:

```bash
cd ~/twitter-telegram-bot

# GitHub'dan çek (eğer GitHub kullanıyorsanız)
git pull

# Veya dosyaları manuel güncelleyin

# Botu restart edin
kill $(cat bot.pid)
bash start_pythonanywhere.sh
```

## 📊 Performans İpuçları

1. **CHECK_INTERVAL** değerini artırın (120-300 saniye)
2. **MAX_TWEETS** değerini düşük tutun (5-10)
3. Çok fazla anahtar kelime kullanmayın (3-5 ideal)
4. Sessiz saatleri kullanın (gece bildirimleri kapatın)

## ✅ Başarı Kontrol Listesi

- [ ] PythonAnywhere hesabı oluşturuldu
- [ ] Kod yüklendi
- [ ] Virtual environment kuruldu
- [ ] Bağımlılıklar yüklendi
- [ ] .env dosyası yapılandırıldı
- [ ] Bot test edildi
- [ ] Telegram bildirimi geldi
- [ ] Always-on task ayarlandı
- [ ] 24 saat sorunsuz çalıştı

## 🆘 Destek

Sorun yaşıyorsanız:
1. Log dosyalarını kontrol edin
2. .env dosyasını doğrulayın
3. PythonAnywhere forum'larına bakın
4. GitHub Issues açın

---

**🎉 Tebrikler!** Botunuz artık MacBook'tan bağımsız 7/24 çalışıyor!
