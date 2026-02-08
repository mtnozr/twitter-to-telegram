#!/bin/bash
# Twitter Telegram Bot Başlatma Scripti

cd "$(dirname "$0")"

echo "🚀 Twitter Telegram Bot Başlatılıyor..."
echo ""

# Bot zaten çalışıyor mu kontrol et
if pgrep -f "python.*bot.py" > /dev/null; then
    echo "⚠️  Bot zaten çalışıyor!"
    echo ""
    echo "Durdurmak için: ./stop_bot.sh"
    exit 1
fi

# Gerekli dosyaları kontrol et
if [ ! -f "twitter_cookies.json" ]; then
    echo "❌ twitter_cookies.json bulunamadı!"
    echo "Lütfen önce: python save_cookies.py"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ .env dosyası bulunamadı!"
    exit 1
fi

# Botu arka planda başlat
nohup python3 bot.py > bot.log 2>&1 &
BOT_PID=$!

sleep 3

# Başarılı mı kontrol et
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Bot başarıyla başlatıldı!"
    echo "📋 Process ID: $BOT_PID"
    echo "📁 Log dosyası: bot.log"
    echo ""
    echo "📊 Durumu görmek için: tail -f bot.log"
    echo "⏹️  Durdurmak için: ./stop_bot.sh"

    # PID'yi kaydet
    echo $BOT_PID > bot.pid
else
    echo "❌ Bot başlatılamadı!"
    echo "Log dosyasını kontrol edin: cat bot.log"
    exit 1
fi
