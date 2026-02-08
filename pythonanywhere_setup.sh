#!/bin/bash
# PythonAnywhere Kurulum Scripti
# Bu scripti PythonAnywhere bash console'da çalıştırın

echo "🚀 Twitter-Telegram Bot - PythonAnywhere Kurulumu"
echo "=================================================="
echo ""

# Mevcut dizini kontrol et
if [ ! -f "bot.py" ]; then
    echo "❌ Hata: bot.py bulunamadı!"
    echo "Lütfen bu scripti bot klasöründe çalıştırın"
    exit 1
fi

echo "📦 Virtual environment oluşturuluyor..."
python3 -m venv venv

echo "✅ Virtual environment oluşturuldu"
echo ""

echo "🔧 Virtual environment aktifleştiriliyor..."
source venv/bin/activate

echo "📥 pip güncelleniyor..."
pip install --upgrade pip --quiet

echo "📥 Bağımlılıklar yükleniyor..."
pip install -r requirements.txt

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "📝 Sonraki adımlar:"
echo "1. .env dosyasını düzenleyin:"
echo "   nano .env"
echo ""
echo "2. Telegram bot token ve chat ID'nizi girin"
echo "3. Anahtar kelimeleri ayarlayın"
echo ""
echo "4. Botu test edin:"
echo "   source venv/bin/activate"
echo "   python bot.py"
echo ""
echo "5. Çalışıyorsa, PythonAnywhere'de Always-on task olarak ayarlayın"
echo ""
