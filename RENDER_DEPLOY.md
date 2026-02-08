# Render.com Deployment Rehberi 🚀

Twitter-Telegram botunuzu Render.com'da **tamamen ücretsiz** 7/24 çalıştırma rehberi.

## ✨ Neden Render.com?

- ✅ **Tamamen ücretsiz**
- ✅ 7/24 çalışma
- ✅ Otomatik GitHub deploy
- ✅ Kolay kurulum (5 dakika)
- ✅ Otomatik restart
- ⚠️ 15 dk inaktiviteden sonra uyur (ama bot sürekli aktif olduğu için sorun olmaz)

---

## 🎯 Adım Adım Kurulum

### 1️⃣ GitHub'a Yeni Dosyaları Push Edin

**MacBook'ta:**

```bash
cd ~/twitter-telegram-bot-pythonanywhere

# Yeni dosyaları ekle
git add Procfile runtime.txt RENDER_DEPLOY.md
git commit -m "Add Render.com deployment files"
git push
```

### 2️⃣ Render.com Hesabı Oluşturun

1. https://render.com adresine gidin
2. **"Get Started for Free"** tıklayın
3. **"Sign up with GitHub"** seçin
4. GitHub ile giriş yapın ve yetkilendirin

### 3️⃣ Yeni Web Service Oluşturun

1. Dashboard'da **"New +"** → **"Web Service"** tıklayın
2. GitHub repo'nuzu bulun: **"twitter-to-telegram"**
3. **"Connect"** tıklayın

### 4️⃣ Service Ayarlarını Yapın

**Name:** `twitter-telegram-bot` (veya istediğiniz isim)

**Region:** `Frankfurt (EU Central)` (size en yakın)

**Branch:** `main`

**Runtime:** `Python 3`

**Build Command:** 
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python bot.py
```

**Instance Type:** **Free** seçin

### 5️⃣ Environment Variables Ekleyin

**"Advanced"** → **"Add Environment Variable"** tıklayın:

```
TELEGRAM_BOT_TOKEN = 8275618891:AAGuKbe0BLlX4oQmyV0Ab0TDdFAiemLSvLM
TELEGRAM_CHAT_ID = 5901227222
SEARCH_KEYWORDS = test
CHECK_INTERVAL = 120
MAX_TWEETS = 10
TWEET_LANGUAGE = all
SILENT_START = 23:00
SILENT_END = 08:00
```

### 6️⃣ Deploy Edin!

**"Create Web Service"** butonuna tıklayın.

**Deploy süreci:**
- ⏳ Build başlayacak (1-2 dakika)
- ✅ Deploy tamamlanacak
- 🚀 Bot otomatik başlayacak

**Telegram'dan bildirim gelecek:**
```
✅ BOT BAŞLATILDI (PythonAnywhere)
```

---

## 📊 Render.com Dashboard

**Logs:** Gerçek zamanlı bot loglarını görebilirsiniz

**Metrics:** CPU, Memory kullanımı

**Manual Deploy:** Kod değiştiğinde otomatik deploy olur

---

## 🔄 Güncelleme

Kod değiştirdiğinizde:

```bash
git add .
git commit -m "Update bot"
git push
```

Render otomatik deploy eder!

---

## ⚠️ Önemli Notlar

1. **15 Dakika Kuralı:** Bot 15 dk hiç istek almazsa uyur. Ama tweet botu sürekli aktif olduğu için sorun olmaz.

2. **Ücretsiz Limitler:**
   - 750 saat/ay (7/24 için yeterli)
   - 512 MB RAM
   - Shared CPU

3. **Restart:** Render otomatik restart yapar, manuel restart gerekmez.

---

## ✅ Başarı Kontrolü

- [ ] Render.com hesabı oluşturuldu
- [ ] GitHub repo bağlandı
- [ ] Environment variables eklendi
- [ ] Deploy tamamlandı
- [ ] Telegram'dan bildirim geldi
- [ ] Bot çalışıyor

---

## 🆘 Sorun Giderme

**Deploy başarısız:**
- Logs'u kontrol edin
- requirements.txt doğru mu?
- Environment variables eklenmiş mi?

**Bot çalışmıyor:**
- Logs'da hata var mı?
- Telegram token doğru mu?

**Bot uyuyor:**
- Normal, 15 dk sonra ilk tweet geldiğinde uyanır

---

## 🎉 Tebrikler!

Botunuz artık Render.com'da **tamamen ücretsiz** 7/24 çalışıyor!
