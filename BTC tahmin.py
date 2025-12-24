import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# AYARLAR
sembol = "BTC-USD"  # İstediğin coin/hisse
kisa_vade = 50      # Örn: 7 yaparsan daha hızlı tepki verir
uzun_vade = 200     # Örn: 25 yaparsan daha hızlı tepki verir

print(f"--- {sembol} İÇİN CANLI TAKİP BAŞLATILIYOR ---")
print("Durdurmak için: CTRL + C tuşlarına bas.")

def sinyal_kontrol():
    # Son 1 günlük veriyi, 1 dakikalık mumlarla çek
    data = yf.download(sembol, period="1d", interval="1m", progress=False)
    
    if len(data) < uzun_vade:
        print("Yeterli veri birikmedi, bekleniyor...")
        return

    # Ortalamaları Hesapla
    data['SMA_Kisa'] = data['Close'].rolling(window=kisa_vade).mean()
    data['SMA_Uzun'] = data['Close'].rolling(window=uzun_vade).mean()

    # Son anlık değerleri al
    son_fiyat = data['Close'].iloc[-1]
    son_kisa = data['SMA_Kisa'].iloc[-1]
    son_uzun = data['SMA_Uzun'].iloc[-1]
    
    # Zaman damgası
    simdi = datetime.now().strftime("%H:%M:%S")

    # Sinyal Mantığı
    durum = "BEKLEMEDE"
    renk = "" # Terminal renklendirmesi opsiyoneldir, burada basit tutuyoruz.
    
    if son_kisa > son_uzun:
        durum = "!!! AL SİNYALİ (BOĞA) !!!"
    elif son_kisa < son_uzun:
        durum = "!!! SAT SİNYALİ (AYI) !!!"

    # Ekrana Bas
    # .item() kullanarak veriyi saf sayıya çeviriyoruz ki ekranda düzgün dursun
    print(f"[{simdi}] Fiyat: {son_fiyat.item():.2f} $ | Kısa Ort: {son_kisa.item():.2f} | Uzun Ort: {son_uzun.item():.2f} -> {durum}")

# SONSUZ DÖNGÜ
while True:
    try:
        sinyal_kontrol()
        # 60 Saniye bekle (Yahoo'yu çok darlayıp ban yememek için)
        time.sleep(60) 
    except Exception as e:
        print(f"Bir hata oldu: {e}")
        time.sleep(10)