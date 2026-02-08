#!/bin/bash
# Twitter Telegram Bot Durdurma Scripti

cd "$(dirname "$0")"

echo "⏹️  Bot durduruluyor..."
echo ""

# PID dosyasından oku
if [ -f "bot.pid" ]; then
    BOT_PID=$(cat bot.pid)
    if ps -p $BOT_PID > /dev/null; then
        kill $BOT_PID
        echo "✅ Bot durduruldu (PID: $BOT_PID)"
        rm bot.pid
    else
        echo "⚠️  Bot zaten çalışmıyor (PID: $BOT_PID)"
        rm bot.pid
    fi
else
    # PID dosyası yoksa tüm bot processlerini bul ve durdur
    PIDS=$(pgrep -f "python.*bot.py")
    if [ -z "$PIDS" ]; then
        echo "ℹ️  Çalışan bot bulunamadı"
    else
        echo "Bot processleri bulundu: $PIDS"
        pkill -f "python.*bot.py"
        echo "✅ Tüm bot processleri durduruldu"
    fi
fi
