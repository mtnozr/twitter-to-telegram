#!/usr/bin/env python3
"""
Telegram Bot Commands Handler
Telegram'dan bot kontrolü için komut yöneticisi - Soru-Cevap Sistemi
"""

import os
import logging
from datetime import datetime
from dotenv import set_key
import requests

logger = logging.getLogger(__name__)


class TelegramCommandHandler:
    def __init__(self, telegram_token, chat_id, bot_instance=None):
        self.token = telegram_token
        self.chat_id = chat_id
        self.bot_instance = bot_instance
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        self.env_file = '.env'

        # Conversation state (hangi sorunun cevabını bekliyoruz?)
        self.waiting_for = None  # 'keywords', 'language', None

    def get_updates(self):
        """Telegram'dan yeni mesajları al"""
        try:
            response = requests.get(
                f"{self.api_url}/getUpdates",
                params={'offset': self.last_update_id + 1, 'timeout': 1},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('result', [])
        except Exception as e:
            logger.error(f"Update alma hatası: {e}")
        return []

    def send_message(self, text, reply_markup=None):
        """Telegram'a mesaj gönder"""
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': text
            }
            if reply_markup:
                payload['reply_markup'] = reply_markup

            response = requests.post(
                f"{self.api_url}/sendMessage",
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Mesaj gönderme hatası: {e}")
            return False

    def handle_response(self, text):
        """Kullanıcı cevabını işle"""
        if self.waiting_for == 'keywords':
            # Kelimeleri kaydet
            set_key(self.env_file, 'SEARCH_KEYWORDS', text)

            # Bot instance'ının keywords'ünü anında güncelle
            if self.bot_instance:
                from dotenv import load_dotenv
                load_dotenv(override=True)
                keywords_raw = os.getenv('SEARCH_KEYWORDS', '')
                self.bot_instance.keywords = [k.strip().strip("'\"") for k in keywords_raw.split(',')]

                keyword_list = ', '.join(self.bot_instance.keywords)
                self.send_message(
                    f"✅ Kelimeler güncellendi!\n\n"
                    f"🔍 Yeni kelimeler: {keyword_list}\n\n"
                    f"✨ Değişiklik hemen geçerli oldu!\n"
                    f"(Yeniden başlatmaya gerek yok)"
                )
            else:
                self.send_message(
                    f"✅ Kelimeler kaydedildi!\n\n"
                    f"🔍 Yeni kelimeler: {text}\n\n"
                    f"⚠️ Değişikliklerin geçerli olması için:\n"
                    f"/durdur → /başlat"
                )

            self.waiting_for = None

        elif self.waiting_for == 'language':
            # Dil seçimini kaydet
            lang_map = {
                'tr': 'tr', 'türkçe': 'tr', 'turkish': 'tr', '1': 'tr',
                'en': 'en', 'ingilizce': 'en', 'english': 'en', '2': 'en',
                'tümü': 'all', 'all': 'all', 'hepsi': 'all', '3': 'all'
            }

            selected = lang_map.get(text.lower())

            if selected:
                set_key(self.env_file, 'TWEET_LANGUAGE', selected)

                # Bot instance'ının dil ayarını anında güncelle
                if self.bot_instance:
                    from dotenv import load_dotenv
                    load_dotenv(override=True)
                    self.bot_instance.tweet_language = os.getenv('TWEET_LANGUAGE', 'all')

                lang_names = {'tr': '🇹🇷 Türkçe', 'en': '🇬🇧 İngilizce', 'all': '🌍 Tümü'}
                self.send_message(
                    f"✅ Dil güncellendi: {lang_names[selected]}\n\n"
                    f"✨ Değişiklik hemen geçerli oldu!\n"
                    f"(Yeniden başlatmaya gerek yok)"
                )
                self.waiting_for = None
            else:
                self.send_message(
                    "❌ Geçersiz seçim!\n\n"
                    "Lütfen şunlardan birini yazın:\n"
                    "1️⃣ TR (Türkçe)\n"
                    "2️⃣ EN (İngilizce)\n"
                    "3️⃣ Tümü (Tüm diller)"
                )

    def handle_command(self, text):
        """Komutları işle"""
        command = text.lower().split()[0]

        if command == '/kelime':
            return self.cmd_kelime()
        elif command == '/dil':
            return self.cmd_dil()
        elif command == '/durdur':
            return self.cmd_durdur()
        elif command in ['/başlat', '/baslat']:
            return self.cmd_baslat()
        elif command in ['/sessiz', '/sesli']:
            return self.cmd_sessiz()
        elif command == '/durum':
            return self.cmd_durum()
        elif command == '/help':
            return self.cmd_help()
        else:
            return "❌ Bilinmeyen komut. /help yazın."

    def cmd_help(self):
        """Yardım mesajı"""
        msg = """
🤖 TELEGRAM BOT KOMUTLARI

🔍 /kelime
   Takip edilecek kelimeleri ayarla

🌍 /dil
   Tweet dilini seç (TR/EN/Tümü)

🔕 /sessiz
   Sessiz saatleri aç/kapat (23:00-08:00)

⏸️ /durdur
   Tweet takibini durdur

▶️ /başlat
   Tweet takibini başlat

📊 /durum
   Mevcut ayarları göster

❓ /help
   Bu yardım mesajı

━━━━━━━━━━━━━━━
💡 Kullanım çok basit!
Sadece komutu yazın, bot size soru sorar, siz cevaplarsınız!
        """.strip()

        # Butonlar ekle
        keyboard = {
            'keyboard': [
                [{'text': '/durum'}, {'text': '/help'}],
                [{'text': '/başlat'}, {'text': '/durdur'}],
                [{'text': '/kelime'}, {'text': '/dil'}],
                [{'text': '/sessiz'}]
            ],
            'resize_keyboard': True,
            'one_time_keyboard': False
        }

        self.send_message(msg, reply_markup=keyboard)
        return None  # Zaten gönderildi

    def cmd_kelime(self):
        """Kelime değiştir - Soru-cevap modu"""
        self.waiting_for = 'keywords'

        current = os.getenv('SEARCH_KEYWORDS', '')
        if current:
            keywords = [k.strip().strip("'\"") for k in current.split(',')]
            current_text = ', '.join(keywords)
        else:
            current_text = '❌ Henüz kelime yok'

        msg = (
            f"🔍 ANAHTAR KELİMELER\n\n"
            f"📋 Şu anki kelimeler:\n{current_text}\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"Takip etmek istediğiniz kelimeleri yazın:\n\n"
            f"💡 ÖRNEKLER:\n\n"
            f"1️⃣ Basit arama:\n"
            f"   bitcoin\n\n"
            f"2️⃣ Her iki kelime de geçmeli:\n"
            f"   vakıfbank AND atm\n"
            f"   (veya: vakıfbank atm)\n\n"
            f"3️⃣ En az biri geçmeli:\n"
            f"   bitcoin OR ethereum\n\n"
            f"4️⃣ Tam ifade:\n"
            f"   \"kripto para\"\n\n"
            f"5️⃣ Hariç tutma:\n"
            f"   bitcoin -scam\n\n"
            f"6️⃣ Birden fazla arama (virgülle):\n"
            f"   vakıfbank atm,garanti atm\n\n"
            f"ℹ️ Büyük/küçük harf fark etmez!"
        )
        self.send_message(msg)

    def cmd_dil(self):
        """Dil değiştir - Soru-cevap modu"""
        self.waiting_for = 'language'

        current = os.getenv('TWEET_LANGUAGE', 'all')
        lang_names = {'tr': '🇹🇷 Türkçe', 'en': '🇬🇧 İngilizce', 'all': '🌍 Tümü'}

        msg = (
            f"🌍 DİL SEÇİMİ\n\n"
            f"📋 Şu anki dil: {lang_names.get(current, 'Tümü')}\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"Hangi dilde tweet'leri takip etmek istersiniz?\n\n"
            f"1️⃣ TR (Türkçe tweet'ler)\n"
            f"2️⃣ EN (İngilizce tweet'ler)\n"
            f"3️⃣ Tümü (Tüm diller)\n\n"
            f"Seçiminizi yazın (1, 2, 3 veya TR, EN, Tümü)"
        )
        self.send_message(msg)

    def cmd_durdur(self):
        """Tweet takibini durdur"""
        if not self.bot_instance:
            return "❌ Bot instance bulunamadı!"

        if not self.bot_instance.monitoring_enabled:
            return "ℹ️ Tweet takibi zaten durmuş.\n\n/başlat ile başlatabilirsiniz."

        self.bot_instance.monitoring_enabled = False

        return (
            f"⏸️ TWEET TAKİBİ DURDURULDU\n\n"
            f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            f"✅ Bot çalışıyor ama tweet aramıyor\n"
            f"✅ Telegram komutlarını alıyor\n\n"
            f"▶️ Devam etmek için: /başlat"
        )

    def cmd_baslat(self):
        """Tweet takibini başlat"""
        if not self.bot_instance:
            return "❌ Bot instance bulunamadı!"

        if self.bot_instance.monitoring_enabled:
            return "ℹ️ Tweet takibi zaten çalışıyor!"

        self.bot_instance.monitoring_enabled = True

        keywords = os.getenv('SEARCH_KEYWORDS', '')
        if keywords:
            keyword_list = [k.strip().strip("'\"") for k in keywords.split(',')]
            kw_text = ', '.join(keyword_list)
        else:
            kw_text = '❌ Kelime yok'

        language = os.getenv('TWEET_LANGUAGE', 'all')
        lang_names = {'tr': '🇹🇷 Türkçe', 'en': '🇬🇧 İngilizce', 'all': '🌍 Tümü'}

        return (
            f"▶️ TWEET TAKİBİ BAŞLATILDI\n\n"
            f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            f"🔍 Kelimeler: {kw_text}\n"
            f"🌍 Dil: {lang_names.get(language, 'Tümü')}\n\n"
            f"✅ Yeni tweet'ler Telegram'a gönderilecek!\n\n"
            f"⏸️ Durdurmak için: /durdur"
        )

    def cmd_sessiz(self):
        """Sessiz saatleri aç/kapat (switch)"""
        silent_start = os.getenv('SILENT_START', '')
        silent_end = os.getenv('SILENT_END', '')

        # Sessiz mod açık mı?
        if silent_start and silent_end:
            # Kapat
            set_key(self.env_file, 'SILENT_START', '')
            set_key(self.env_file, 'SILENT_END', '')

            # Bot instance'ını güncelle
            if self.bot_instance:
                from dotenv import load_dotenv
                load_dotenv(override=True)
                self.bot_instance.silent_start = ''
                self.bot_instance.silent_end = ''

            return (
                f"🔔 SESSİZ MOD KAPATILDI\n\n"
                f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
                f"✅ Artık tüm saatlerde bildirim gelecek!\n\n"
                f"✨ Değişiklik hemen geçerli oldu!"
            )
        else:
            # Aç (default: 23:00 - 08:00)
            set_key(self.env_file, 'SILENT_START', '23:00')
            set_key(self.env_file, 'SILENT_END', '08:00')

            # Bot instance'ını güncelle
            if self.bot_instance:
                from dotenv import load_dotenv
                load_dotenv(override=True)
                self.bot_instance.silent_start = '23:00'
                self.bot_instance.silent_end = '08:00'

            return (
                f"🔕 SESSİZ MOD AÇILDI\n\n"
                f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
                f"🌙 23:00 - 08:00 arası bildirim GELMEYECEK\n"
                f"✅ Diğer saatlerde normal bildirim gelecek!\n\n"
                f"✨ Değişiklik hemen geçerli oldu!"
            )

    def cmd_durum(self):
        """Bot durumunu göster"""
        keywords = os.getenv('SEARCH_KEYWORDS', '')
        if keywords:
            keyword_list = [k.strip().strip("'\"") for k in keywords.split(',')]
            kw_text = '\n'.join([f"  • {k}" for k in keyword_list])
        else:
            kw_text = '  ❌ Henüz kelime yok'

        language = os.getenv('TWEET_LANGUAGE', 'all')
        lang_names = {'tr': '🇹🇷 Türkçe', 'en': '🇬🇧 İngilizce', 'all': '🌍 Tümü'}

        interval = os.getenv('CHECK_INTERVAL', '60')
        silent_start = os.getenv('SILENT_START', '')
        silent_end = os.getenv('SILENT_END', '')

        # Tweet takibi durumu
        if self.bot_instance:
            if self.bot_instance.monitoring_enabled:
                status = "▶️ ÇALIŞIYOR"
            else:
                status = "⏸️ DURDURULMUŞ"
        else:
            status = "❓ BİLİNMİYOR"

        msg = (
            f"📊 BOT DURUMU\n\n"
            f"🤖 Durum: {status}\n\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"🔍 Takip Edilen Kelimeler:\n{kw_text}\n\n"
            f"🌍 Dil: {lang_names.get(language, 'Tümü')}\n"
            f"⏱️ Kontrol Aralığı: {interval} saniye\n"
        )

        if silent_start and silent_end:
            msg += f"🔕 Sessiz Saatler: {silent_start} - {silent_end}\n"
        else:
            msg += f"🔔 Sessiz Saatler: Kapalı\n"

        msg += "\n━━━━━━━━━━━━━━━\n💡 /help - Tüm komutlar"

        return msg

    def process_updates(self):
        """Yeni mesajları işle"""
        updates = self.get_updates()

        for update in updates:
            self.last_update_id = update['update_id']

            if 'message' not in update:
                continue

            message = update['message']

            # Sadece kendi chat_id'mizden gelen mesajları kabul et
            if str(message['chat']['id']) != str(self.chat_id):
                continue

            if 'text' not in message:
                continue

            text = message['text'].strip()

            if not text:
                continue

            # Eğer cevap bekliyorsak (conversation state)
            if self.waiting_for:
                logger.info(f"Cevap alındı ({self.waiting_for}): {text}")
                self.handle_response(text)
                continue

            # Komut mu kontrol et
            if text.startswith('/'):
                logger.info(f"Komut alındı: {text}")
                response = self.handle_command(text)
                if response:
                    self.send_message(response)
