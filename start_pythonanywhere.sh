#!/bin/bash
# PythonAnywhere'de botu başlatma scripti

echo "🚀 Twitter-Telegram Bot başlatılıyor..."

# Bot klasörüne git
cd ~/twitter-telegram-bot

# Virtual environment'ı aktifleştir
source venv/bin/activate

# Eski process varsa temizle
if [ -f bot.pid ]; then
    OLD_PID=$(cat bot.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  Eski bot process'i durduruluyor (PID: $OLD_PID)..."
        kill $OLD_PID
        sleep 2
    fi
    rm bot.pid
fi

# Log dosyasını temizle (opsiyonel)
if [ -f bot.log ]; then
    # Son 1000 satırı sakla
    tail -n 1000 bot.log > bot.log.tmp
    mv bot.log.tmp bot.log
fi

# Botu arka planda başlat
echo "▶️  Bot başlatılıyor..."
nohup python bot.py > bot.log 2>&1 &
echo $! > bot.pid

echo ""
echo "✅ Bot başlatıldı!"
echo "📋 Process ID: $(cat bot.pid)"
echo ""
echo "📊 Durumu kontrol etmek için:"
echo "   tail -f bot.log"
echo ""
echo "🛑 Durdurmak için:"
echo "   kill \$(cat bot.pid)"
echo ""
