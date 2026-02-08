#!/usr/bin/env python3
"""
Twitter (X) to Telegram Bot - PythonAnywhere Version
Belirli kelimeleri Twitter'da arar ve yeni tweet'leri Telegram'a gönderir.
snscrape kullanır (login gerektirmez, PythonAnywhere uyumlu).
"""

import os
import time
import logging
import asyncio
import signal
from datetime import datetime, time as dtime
from dotenv import load_dotenv
import requests
from telegram_commands import TelegramCommandHandler

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TwitterTelegramBot:
    def __init__(self):
        """Bot'u başlat ve bağlantıları kur"""
        # .env dosyasını yükle (override=True ile her başlatmada fresh oku)
        load_dotenv(override=True)

        # Telegram Bot bağlantısı
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not self.telegram_token or not self.telegram_chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID bulunamadı!")

        self.telegram_api_url = f"https://api.telegram.org/bot{self.telegram_token}"

        # Ayarlar
        # Kelimeleri oku ve temizle (tırnak ve boşlukları kaldır)
        keywords_raw = os.getenv('SEARCH_KEYWORDS', 'python')
        self.keywords = [k.strip().strip("'\"") for k in keywords_raw.split(',')]
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '60'))
        self.max_tweets = int(os.getenv('MAX_TWEETS', '10'))
        self.tweet_language = os.getenv('TWEET_LANGUAGE', 'all')

        # Son kontrol edilen tweet ID'lerini sakla
        self.last_tweet_ids = {}
        self.history_file = 'tweet_history.json'
        self.load_history()

        # Sessiz saatler
        self.silent_start = os.getenv('SILENT_START', '')
        self.silent_end = os.getenv('SILENT_END', '')

        # Bot durumu
        self.is_running = True
        self.monitoring_enabled = True  # Tweet takibi aktif mi? (/durdur ile kapatılabilir)
        self.shutdown_reason = None

        # Telegram komut handler (bot_instance=self ile bot kontrolü için)
        self.command_handler = TelegramCommandHandler(
            self.telegram_token,
            self.telegram_chat_id,
            bot_instance=self
        )

        logger.info(f"🚀 Bot başlatıldı (PythonAnywhere Version)")
        logger.info(f"🔍 Anahtar kelimeler: {self.keywords}")
        logger.info(f"⏱️  Kontrol aralığı: {self.check_interval} saniye")
        if self.silent_start and self.silent_end:
            logger.info(f"🔕 Sessiz saatler: {self.silent_start} - {self.silent_end}")

    def load_history(self):
        """Tweet geçmişini yükle"""
        import json
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.last_tweet_ids = json.load(f)
                logger.info(f"📚 Geçmiş yüklendi: {len(self.last_tweet_ids)} keyword")
            else:
                logger.info("📝 Yeni geçmiş dosyası oluşturulacak")
        except Exception as e:
            logger.error(f"Geçmiş yükleme hatası: {e}")

    def save_history(self):
        """Tweet geçmişini kaydet"""
        import json
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.last_tweet_ids, f, indent=2)
            logger.debug("💾 Geçmiş kaydedildi")
        except Exception as e:
            logger.error(f"Geçmiş kaydetme hatası: {e}")

    def search_tweets(self, keyword):
        """snscrape ile tweet ara"""
        try:
            import snscrape.modules.twitter as sntwitter
            
            keyword = keyword.strip()
            logger.info(f"'{keyword}' için tweet aranıyor...")

            # Dil filtresi ekle
            query = keyword
            if self.tweet_language != 'all':
                query = f"{keyword} lang:{self.tweet_language}"

            tweets = []
            
            # snscrape ile tweet'leri çek
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= self.max_tweets:
                    break
                
                # Retweet'leri atla
                if hasattr(tweet, 'retweetedTweet') and tweet.retweetedTweet:
                    continue
                
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.rawContent,
                    'created_at': tweet.date,
                    'author_name': tweet.user.displayname,
                    'author_username': tweet.user.username,
                    'likes': tweet.likeCount or 0,
                    'retweets': tweet.retweetCount or 0,
                    'url': tweet.url
                })

            logger.info(f"✅ {len(tweets)} tweet bulundu")
            return tweets

        except Exception as e:
            logger.error(f"❌ Tweet arama hatası: {e}")
            return []

    def is_silent_hours(self):
        """Sessiz saatlerde mi kontrol et"""
        if not self.silent_start or not self.silent_end:
            return False

        try:
            now = datetime.now().time()
            start = datetime.strptime(self.silent_start, '%H:%M').time()
            end = datetime.strptime(self.silent_end, '%H:%M').time()

            # Gece yarısını geçen durum (örn: 23:00 - 08:00)
            if start > end:
                return now >= start or now <= end
            else:
                return start <= now <= end
        except Exception as e:
            logger.error(f"Sessiz saat kontrolü hatası: {e}")
            return False

    def send_telegram_message(self, tweet, keyword):
        """Telegram'a mesaj gönder"""
        try:
            # Sessiz saatlerde mesaj gönderme
            if self.is_silent_hours():
                logger.info(f"🔕 Sessiz saatlerde - mesaj gönderilmedi: {tweet['id']}")
                return False
            
            text = tweet['text']
            if len(text) > 300:
                text = text[:297] + "..."

            # Tarih formatı
            tweet_date = tweet['created_at']
            date_str = tweet_date.strftime('%d.%m.%Y')
            time_str = tweet_date.strftime('%H:%M')

            message = f"""
🐦 Yeni Tweet Bulundu!

🔍 Anahtar Kelime: {keyword}

👤 {tweet['author_name']} (@{tweet['author_username']})
📝 {text}

📊 ❤️ {tweet['likes']} beğeni | 🔄 {tweet['retweets']} retweet

📅 Tweet Tarihi: {date_str} - {time_str}
🔗 {tweet['url']}
            """.strip()

            response = requests.post(
                f"{self.telegram_api_url}/sendMessage",
                json={
                    'chat_id': self.telegram_chat_id,
                    'text': message,
                    'disable_web_page_preview': False
                },
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"✅ Telegram mesajı gönderildi: {tweet['id']}")
                return True
            else:
                logger.error(f"❌ Telegram hatası: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Mesaj gönderme hatası: {e}")
            return False

    async def process_keyword(self, keyword):
        """Bir anahtar kelime için işlem yap"""
        keyword = keyword.strip()

        tweets = self.search_tweets(keyword)

        if not tweets:
            logger.info(f"'{keyword}' için tweet bulunamadı")
            return

        # Son görülen tweet ID'sini al
        last_id = self.last_tweet_ids.get(keyword, 0)

        # İlk çalıştırma: Sadece referans noktası oluştur, mesaj gönderme
        if last_id == 0:
            # En yeni tweet'i referans noktası olarak kaydet
            newest_tweet_id = max([int(t['id']) for t in tweets])
            self.last_tweet_ids[keyword] = newest_tweet_id
            self.save_history()
            logger.info(f"'{keyword}' için başlangıç referans noktası: {newest_tweet_id}")
            logger.info(f"'{keyword}' - Bundan sonraki tweet'ler bildirilecek")
            return

        new_tweets = [t for t in tweets if int(t['id']) > last_id]

        if not new_tweets:
            logger.info(f"'{keyword}' için yeni tweet yok")
            return

        # Yeni tweet'leri eskiden yeniye sırala
        new_tweets.sort(key=lambda x: int(x['id']))

        # Her yeni tweet için Telegram bildirimi gönder
        sent_count = 0
        for tweet in new_tweets:
            if self.send_telegram_message(tweet, keyword):
                sent_count += 1
            await asyncio.sleep(2)

        # En son tweet ID'sini güncelle ve kaydet
        if new_tweets:
            self.last_tweet_ids[keyword] = int(new_tweets[-1]['id'])
            self.save_history()  # Dosyaya kaydet
            logger.info(f"'{keyword}' için {sent_count} yeni tweet gönderildi")

    def send_notification(self, message):
        """Telegram'a bildirim gönder"""
        try:
            requests.post(
                f"{self.telegram_api_url}/sendMessage",
                json={'chat_id': self.telegram_chat_id, 'text': message},
                timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"Bildirim gönderme hatası: {e}")
            return False

    async def check_commands(self):
        """Telegram komutlarını kontrol et"""
        while self.is_running:
            try:
                self.command_handler.process_updates()
                await asyncio.sleep(2)  # Her 2 saniyede bir kontrol et
            except Exception as e:
                logger.error(f"Komut kontrol hatası: {e}")
                await asyncio.sleep(5)

    async def run(self):
        """Bot'u sürekli çalıştır"""
        try:
            # Başlatma mesajı gönder
            silent_info = ""
            if self.silent_start and self.silent_end:
                silent_info = f"\n🔕 Sessiz: {self.silent_start} - {self.silent_end}"

            startup_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            self.send_notification(
                f"✅ BOT BAŞLATILDI (PythonAnywhere)\n\n"
                f"⏰ {startup_time}\n"
                f"🔍 Kelimeler: {', '.join(self.keywords)}\n"
                f"🌍 Dil: {self.tweet_language.upper()}{silent_info}\n\n"
                f"💡 Komutlar: /help"
            )

            logger.info("🚀 Bot çalışmaya başladı...")

            # Komut dinleyici task'ı başlat
            command_task = asyncio.create_task(self.check_commands())

            # Ana döngü
            while self.is_running:
                try:
                    # Tweet monitoring sadece enabled ise çalışır
                    if self.monitoring_enabled:
                        for keyword in self.keywords:
                            if not self.is_running:
                                break
                            await self.process_keyword(keyword)
                            await asyncio.sleep(3)

                        if not self.is_running:
                            break

                        logger.info(f"⏳ {self.check_interval} saniye bekleniyor...")

                        # Beklemeyi 5 saniyelik parçalara böl (signal alındığında hızlı çıkış için)
                        remaining = self.check_interval
                        while remaining > 0 and self.is_running:
                            sleep_time = min(5, remaining)
                            await asyncio.sleep(sleep_time)
                            remaining -= sleep_time
                    else:
                        # Monitoring kapalıysa sadece kısa süre bekle (telegram komutları için)
                        await asyncio.sleep(5)

                except Exception as e:
                    logger.error(f"Döngü hatası: {e}")
                    await asyncio.sleep(10)

        except KeyboardInterrupt:
            self.shutdown_reason = "Manuel durdurma (Ctrl+C)"
            logger.info(self.shutdown_reason)
        except Exception as e:
            self.shutdown_reason = f"Hata: {str(e)}"
            logger.error(f"Bot hatası: {e}")
        finally:
            self.is_running = False

            # Durdurma mesajı gönder
            shutdown_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            reason = self.shutdown_reason or "Bilinmeyen sebep"

            self.send_notification(
                f"⛔ BOT DURDURULDU\n\n"
                f"⏰ {shutdown_time}\n"
                f"📋 Sebep: {reason}\n\n"
                f"💡 Yeniden başlatmak için:\n"
                f"• PythonAnywhere'de restart edin"
            )


async def main():
    """Ana fonksiyon"""
    bot = None
    try:
        bot = TwitterTelegramBot()

        # Signal handler'ları ayarla
        def signal_handler(signum, frame):
            logger.info(f"Signal alındı: {signum}")
            if bot:
                bot.is_running = False
                bot.shutdown_reason = f"Signal durdurma (signal {signum})"

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        await bot.run()

    except Exception as e:
        logger.error(f"Bot hatası: {e}")
        if bot:
            bot.shutdown_reason = f"Beklenmeyen hata: {str(e)}"
        raise


if __name__ == "__main__":
    asyncio.run(main())
