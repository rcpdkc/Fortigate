import requests
import re
import time
from datetime import datetime

def get_ip_addresses_from_url(url):
    total_ips = 0  # Toplam IP sayısını izlemek için sayaç
    try:
        # URL'den metni al
        response = requests.get(url, timeout=10)  # Timeout ekleyerek bekleme süresini belirtin
        # Yanıt başarılıysa devam et
        if response.status_code == 200:
            # Metni satır satır oku
            for line in response.text.splitlines():
                # IP adreslerini regex kullanarak bul
                ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                # Eğer bir IP adresi bulunduysa dosyaya yaz
                if ip_addresses:
                    total_ips += 1
                    with open("usom.txt", "a") as file:
                        file.write(ip_addresses[0] + "\n")  # IP adresini dosyaya yaz
        # Güncelleme tarihi ve toplam IP sayısını çıktı olarak yaz
        print(f"Güncelleme Tarihi: {datetime.now()} | Toplam IP Sayısı: {total_ips}")
    except requests.exceptions.Timeout:
        print("İstek zaman aşımına uğradı. Bağlantı süresini kontrol edin.")
        time.sleep(60)  # 1 dakika bekle
    except requests.exceptions.RequestException as e:
        print("Bir hata oluştu:", e)
        time.sleep(60)  # 1 dakika bekle

while True:
    print("Zararlı web site veri tabanı güncellendi.")
    # URL'den IP adreslerini al ve dosyaya yaz
    get_ip_addresses_from_url("https://www.usom.gov.tr/url-list.txt")
    # 1 dakika bekle
    time.sleep(36000)
