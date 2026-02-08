#!/bin/bash
# Twitter Telegram Bot Durum Kontrolü

cd "$(dirname "$0")"

echo "📊 Twitter Telegram Bot Durumu"
echo "================================"
echo ""

# Bot çalışıyor mu?
if pgrep -f "python.*bot.py" > /dev/null; then
    echo "✅ Bot ÇALIŞIYOR"
    echo ""

    # Process bilgileri
    ps aux | grep "python.*bot.py" | grep -v grep
    echo ""

    # PID dosyası
    if [ -f "bot.pid" ]; then
        echo "📋 PID: $(cat bot.pid)"
    fi

    # Son loglar
    if [ -f "bot.log" ]; then
        echo ""
        echo "📄 Son 10 log satırı:"
        echo "---"
        tail -10 bot.log
    fi
else
    echo "❌ Bot ÇALIŞMIYOR"
    echo ""
    echo "Başlatmak için: ./start_bot.sh"
fi

echo ""
echo "================================"

# Dosya kontrolleri
echo ""
echo "📁 Dosya Durumu:"
[ -f "twitter_cookies.json" ] && echo "✅ twitter_cookies.json" || echo "❌ twitter_cookies.json"
[ -f "tweet_history.json" ] && echo "✅ tweet_history.json" || echo "❌ tweet_history.json"
[ -f ".env" ] && echo "✅ .env" || echo "❌ .env"
[ -f "bot.log" ] && echo "✅ bot.log" || echo "❌ bot.log"
