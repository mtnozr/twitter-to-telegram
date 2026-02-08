#!/usr/bin/env python3
"""
Twitter Bot Ayarlar Yöneticisi - Grafik Arayüz
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from dotenv import load_dotenv, set_key
import subprocess
import signal

class BotSettingsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐦 Twitter Bot Ayarları")
        self.root.geometry("600x750")
        self.root.resizable(False, False)

        # .env dosyasını yükle
        load_dotenv()
        self.env_file = '.env'

        # Script dizini
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Ana frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Başlık
        title_label = ttk.Label(
            main_frame,
            text="🐦 Twitter Telegram Bot Ayarları",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Anahtar Kelimeler
        ttk.Label(
            main_frame,
            text="🔍 Aranacak Kelimeler:",
            font=('Arial', 11, 'bold')
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        ttk.Label(
            main_frame,
            text="(Virgül ile ayırın, örn: bitcoin,ethereum,kripto)",
            font=('Arial', 9),
            foreground='gray'
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W)

        self.keywords_text = scrolledtext.ScrolledText(
            main_frame,
            height=4,
            width=50,
            font=('Arial', 11)
        )
        self.keywords_text.grid(row=3, column=0, columnspan=2, pady=(5, 15))

        # Mevcut değeri yükle
        current_keywords = os.getenv('SEARCH_KEYWORDS', 'python')
        self.keywords_text.insert(1.0, current_keywords)

        # Kontrol Aralığı
        ttk.Label(
            main_frame,
            text="⏱️ Kontrol Aralığı (saniye):",
            font=('Arial', 11, 'bold')
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        interval_frame = ttk.Frame(main_frame)
        interval_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(5, 15))

        self.interval_var = tk.IntVar(value=int(os.getenv('CHECK_INTERVAL', '60')))
        self.interval_scale = ttk.Scale(
            interval_frame,
            from_=30,
            to=300,
            orient=tk.HORIZONTAL,
            length=300,
            variable=self.interval_var,
            command=self.update_interval_label
        )
        self.interval_scale.grid(row=0, column=0, padx=(0, 10))

        self.interval_label = ttk.Label(
            interval_frame,
            text=f"{self.interval_var.get()} saniye",
            font=('Arial', 10, 'bold')
        )
        self.interval_label.grid(row=0, column=1)

        # Max Tweet Sayısı
        ttk.Label(
            main_frame,
            text="📊 Kaç Tweet Kontrol Edilsin:",
            font=('Arial', 11, 'bold')
        ).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        max_tweets_frame = ttk.Frame(main_frame)
        max_tweets_frame.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(5, 15))

        self.max_tweets_var = tk.IntVar(value=int(os.getenv('MAX_TWEETS', '10')))
        self.max_tweets_scale = ttk.Scale(
            max_tweets_frame,
            from_=5,
            to=50,
            orient=tk.HORIZONTAL,
            length=300,
            variable=self.max_tweets_var,
            command=self.update_max_tweets_label
        )
        self.max_tweets_scale.grid(row=0, column=0, padx=(0, 10))

        self.max_tweets_label = ttk.Label(
            max_tweets_frame,
            text=f"{self.max_tweets_var.get()} tweet",
            font=('Arial', 10, 'bold')
        )
        self.max_tweets_label.grid(row=0, column=1)

        # Dil Seçimi
        ttk.Label(
            main_frame,
            text="🌍 Tweet Dili:",
            font=('Arial', 11, 'bold')
        ).grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        language_frame = ttk.Frame(main_frame)
        language_frame.grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(5, 15))

        self.language_var = tk.StringVar(value=os.getenv('TWEET_LANGUAGE', 'all'))

        ttk.Radiobutton(
            language_frame,
            text="🇹🇷 Türkçe",
            variable=self.language_var,
            value='tr'
        ).grid(row=0, column=0, padx=(0, 15))

        ttk.Radiobutton(
            language_frame,
            text="🇬🇧 İngilizce",
            variable=self.language_var,
            value='en'
        ).grid(row=0, column=1, padx=(0, 15))

        ttk.Radiobutton(
            language_frame,
            text="🌍 Tümü",
            variable=self.language_var,
            value='all'
        ).grid(row=0, column=2)

        # Sessiz Saatler
        ttk.Label(
            main_frame,
            text="🔕 Sessiz Saatler:",
            font=('Arial', 11, 'bold')
        ).grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        ttk.Label(
            main_frame,
            text="(Bu saatler arasında bildirim gönderilmez)",
            font=('Arial', 9),
            foreground='gray'
        ).grid(row=11, column=0, columnspan=2, sticky=tk.W)

        silent_frame = ttk.Frame(main_frame)
        silent_frame.grid(row=12, column=0, columnspan=2, sticky=tk.W, pady=(5, 15))

        # Sessiz mod aktif/pasif
        self.silent_enabled = tk.BooleanVar(value=bool(os.getenv('SILENT_START')))
        self.silent_check = ttk.Checkbutton(
            silent_frame,
            text="Sessiz modu aktif et",
            variable=self.silent_enabled,
            command=self.toggle_silent_inputs
        )
        self.silent_check.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 5))

        # Başlangıç saati
        ttk.Label(silent_frame, text="Başlangıç:").grid(row=1, column=0, sticky=tk.W, padx=(20, 5))
        self.silent_start_hour = ttk.Spinbox(silent_frame, from_=0, to=23, width=5, format="%02.0f")
        self.silent_start_hour.grid(row=1, column=1)
        ttk.Label(silent_frame, text=":").grid(row=1, column=2)
        self.silent_start_min = ttk.Spinbox(silent_frame, from_=0, to=59, width=5, format="%02.0f")
        self.silent_start_min.grid(row=1, column=3)

        # Bitiş saati
        ttk.Label(silent_frame, text="Bitiş:").grid(row=2, column=0, sticky=tk.W, padx=(20, 5), pady=(5, 0))
        self.silent_end_hour = ttk.Spinbox(silent_frame, from_=0, to=23, width=5, format="%02.0f")
        self.silent_end_hour.grid(row=2, column=1, pady=(5, 0))
        ttk.Label(silent_frame, text=":").grid(row=2, column=2, pady=(5, 0))
        self.silent_end_min = ttk.Spinbox(silent_frame, from_=0, to=59, width=5, format="%02.0f")
        self.silent_end_min.grid(row=2, column=3, pady=(5, 0))

        # Mevcut değerleri yükle
        silent_start = os.getenv('SILENT_START', '23:00')
        silent_end = os.getenv('SILENT_END', '08:00')

        if silent_start:
            start_parts = silent_start.strip("'\"").split(':')
            if len(start_parts) == 2:
                self.silent_start_hour.set(start_parts[0])
                self.silent_start_min.set(start_parts[1])

        if silent_end:
            end_parts = silent_end.strip("'\"").split(':')
            if len(end_parts) == 2:
                self.silent_end_hour.set(end_parts[0])
                self.silent_end_min.set(end_parts[1])

        self.toggle_silent_inputs()

        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=13, column=0, columnspan=2, pady=(20, 0))

        self.save_button = ttk.Button(
            button_frame,
            text="💾 Kaydet",
            command=self.save_settings,
            width=15
        )
        self.save_button.grid(row=0, column=0, padx=5)

        self.start_button = ttk.Button(
            button_frame,
            text="▶️ Botu Başlat",
            command=self.start_bot,
            width=15
        )
        self.start_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(
            button_frame,
            text="⏹️ Botu Durdur",
            command=self.stop_bot,
            width=15
        )
        self.stop_button.grid(row=0, column=2, padx=5)

        # Durum
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=('Arial', 9),
            foreground='gray'
        )
        self.status_label.grid(row=14, column=0, columnspan=2, pady=(15, 0))

        # Bot durumunu kontrol et
        self.update_status()

    def update_interval_label(self, value):
        """Interval label'ı güncelle"""
        self.interval_label.config(text=f"{int(float(value))} saniye")

    def update_max_tweets_label(self, value):
        """Max tweets label'ı güncelle"""
        self.max_tweets_label.config(text=f"{int(float(value))} tweet")

    def toggle_silent_inputs(self):
        """Sessiz mod input'larını aktif/pasif yap"""
        state = 'normal' if self.silent_enabled.get() else 'disabled'
        self.silent_start_hour.config(state=state)
        self.silent_start_min.config(state=state)
        self.silent_end_hour.config(state=state)
        self.silent_end_min.config(state=state)

    def save_settings(self):
        """Ayarları kaydet"""
        try:
            keywords = self.keywords_text.get(1.0, tk.END).strip()
            interval = int(self.interval_var.get())
            max_tweets = int(self.max_tweets_var.get())
            language = self.language_var.get()

            if not keywords:
                messagebox.showerror("Hata", "Lütfen en az bir anahtar kelime girin!")
                return

            # Sessiz saatler
            if self.silent_enabled.get():
                silent_start = f"{int(float(self.silent_start_hour.get())):02d}:{int(float(self.silent_start_min.get())):02d}"
                silent_end = f"{int(float(self.silent_end_hour.get())):02d}:{int(float(self.silent_end_min.get())):02d}"
            else:
                silent_start = ""
                silent_end = ""

            # .env dosyasını güncelle
            set_key(self.env_file, 'SEARCH_KEYWORDS', keywords)
            set_key(self.env_file, 'CHECK_INTERVAL', str(interval))
            set_key(self.env_file, 'MAX_TWEETS', str(max_tweets))
            set_key(self.env_file, 'TWEET_LANGUAGE', language)
            set_key(self.env_file, 'SILENT_START', silent_start)
            set_key(self.env_file, 'SILENT_END', silent_end)

            messagebox.showinfo(
                "Başarılı",
                "✅ Ayarlar kaydedildi!\n\n⚠️ Değişikliklerin geçerli olması için botu yeniden başlatın."
            )

        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi: {e}")

    def start_bot(self):
        """Botu başlat"""
        try:
            # Bot zaten çalışıyor mu kontrol et
            result = subprocess.run(
                ['pgrep', '-f', 'python.*bot.py'],
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                messagebox.showwarning(
                    "Uyarı",
                    "⚠️ Bot zaten çalışıyor!\n\nÖnce durdurun, sonra başlatın."
                )
                self.update_status()
                return

            # Bot'u direkt başlat (nohup ile)
            bot_script = os.path.join(self.script_dir, 'bot.py')
            log_file = os.path.join(self.script_dir, 'bot.log')

            # PID dosyasını temizle
            pid_file = os.path.join(self.script_dir, 'bot.pid')
            if os.path.exists(pid_file):
                os.remove(pid_file)

            # Botu arka planda başlat
            with open(log_file, 'w') as log:
                process = subprocess.Popen(
                    ['python3', bot_script],
                    cwd=self.script_dir,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True
                )

                # PID'yi kaydet
                with open(pid_file, 'w') as f:
                    f.write(str(process.pid))

            # 2 saniye bekle (bot başlaması için)
            import time
            time.sleep(2)

            # Mesaj göster ve durumu güncelle
            messagebox.showinfo("Başarılı", "✅ Bot başlatıldı!\n\n📱 Telegram'ı kontrol edin.")
            self.update_status()

        except Exception as e:
            messagebox.showerror("Hata", f"Bot başlatılamadı:\n\n{str(e)}")

    def stop_bot(self):
        """Botu durdur"""
        try:
            # Bot çalışıyor mu kontrol et
            result = subprocess.run(
                ['pgrep', '-f', 'python.*bot.py'],
                capture_output=True,
                text=True
            )

            pid_str = result.stdout.strip()
            if not pid_str:
                messagebox.showinfo("Bilgi", "ℹ️ Bot zaten durmuş.")
                self.update_status()
                return

            # Bot processini düzgün kapat (SIGTERM - kapanma mesajı göndermesine izin ver)
            try:
                pid = int(pid_str.split()[0])  # İlk PID'yi al
                os.kill(pid, 15)  # SIGTERM gönder

                # Bot'un kapanmasını bekle (maksimum 5 saniye)
                import time
                for i in range(10):
                    time.sleep(0.5)
                    check = subprocess.run(
                        ['pgrep', '-f', 'python.*bot.py'],
                        capture_output=True,
                        text=True
                    )
                    if not check.stdout.strip():
                        break
                else:
                    # Hala çalışıyorsa zorla öldür
                    os.kill(pid, 9)  # SIGKILL

            except ProcessLookupError:
                pass  # Process zaten durmuş

            # PID dosyasını sil
            pid_file = os.path.join(self.script_dir, 'bot.pid')
            if os.path.exists(pid_file):
                os.remove(pid_file)

            # Durumu güncelle ve mesaj göster
            messagebox.showinfo("Başarılı", "✅ Bot durduruldu!\n\n📱 Telegram'ı kontrol edin.")

            # Messagebox kapandıktan sonra durumu güncelle
            self.update_status()

        except Exception as e:
            messagebox.showerror("Hata", f"Bot durdurulamadı:\n\n{str(e)}")
            self.update_status()

    def update_status(self):
        """Bot durumunu güncelle"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'python.*bot.py'],
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                self.status_label.config(
                    text="🟢 Bot Çalışıyor",
                    foreground='green'
                )
            else:
                self.status_label.config(
                    text="🔴 Bot Durmuş",
                    foreground='red'
                )
        except:
            self.status_label.config(
                text="⚠️ Durum Bilinmiyor",
                foreground='orange'
            )

def main():
    root = tk.Tk()
    app = BotSettingsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
