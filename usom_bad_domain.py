import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def split_file(input_file, output_prefix, num_lines_per_file):
    with open(input_file, 'r') as source_file:
        lines = source_file.readlines()

    num_lines = len(lines)
    num_files = num_lines // num_lines_per_file

    for i in range(num_files):
        start_idx = i * num_lines_per_file
        end_idx = (i + 1) * num_lines_per_file

        output_file_name = f"{output_prefix}_{i + 1}.txt"

        with open(output_file_name, 'w') as output_file:
            output_file.writelines(lines[start_idx:end_idx])

    # Kalan satırları ayrı bir dosyaya yaz
    if num_lines % num_lines_per_file > 0:
        remaining_lines = lines[num_files * num_lines_per_file:]
        remaining_file_name = f"{output_prefix}_kalan.txt"
        with open(remaining_file_name, 'w') as remaining_file:
            remaining_file.writelines(remaining_lines)

while True:
    try:
        # Verileri almak istediğiniz URL
        url = "https://www.usom.gov.tr/url-list.txt"

        # İndirilen verileri bir metin dosyasına yazma işlemi
        response = session.get(url)

        if response.status_code == 200:
            data = response.text

            with open("veriler.txt", "w", encoding="utf-8") as file:
                file.write(data)
            print("USOM veri tabanından veri çekimi yapıldı.")
            
            # Tarih bilgisini ve toplam URL sayısını al
            now = datetime.now()
            total_urls = data.count("\n")
            print(f"Tarih: {now}, Toplam URL Sayısı: {total_urls}")

            # 100.000 satır şeklinde bölme işlemi
            split_file("veriler.txt", "hedef", 130000)

        else:
            print("URL'den veri alınamadı. HTTP durum kodu:", response.status_code)
    except Exception as err:
        print(err)

    # 60 dakika bekle
    time.sleep(60*60)
