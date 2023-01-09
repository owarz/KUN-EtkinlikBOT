import requests
from bs4 import BeautifulSoup
from telegram.bot import Bot
import time

# Telegram botunuza ait token ve kullandığınız kanalın ID bilgilerini girin
bot = Bot('5907885508:AAE9zJtpI01UsBE8qUCxdPUkGC8t0Ah-cSk')
channel_id = ''

# Duyuru ve etkinlik sayfalarının URL bilgilerini girin
duyuru_url = 'https://kapadokya.edu.tr/duyurular'
etkinlik_url = 'https://kapadokya.edu.tr/etkinlikler'

while True:
    # Sayfalara bağlanma isteği gönderiyoruz
    duyuru_response = requests.get(duyuru_url)
    etkinlik_response = requests.get(etkinlik_url)

    # Gelen cevaplardaki HTML kodlarını parse ediyoruz
    duyuru_soup = BeautifulSoup(duyuru_response.text, 'html.parser')
    etkinlik_soup = BeautifulSoup(etkinlik_response.text, 'html.parser')

    # div id=ContentPlaceHolder1_pnl_Duyuru altındaki ilk sıradaki a etiketinin linkini ve h3 etiketinin yazısını alıyoruz
    duyuru_link = duyuru_soup.select_one('#ContentPlaceHolder1_pnl_Duyuru a')['href']
    duyuru_title = duyuru_soup.select_one('#ContentPlaceHolder1_pnl_Duyuru h3').text

    # div id=ContentPlaceHolder1_pnl_Duyuru altındaki ilk sıradaki a etiketinin linkini ve h3 etiketinin yazısını alıyoruz
    etkinlik_link = etkinlik_soup.select_one('#ContentPlaceHolder1_pnl_Duyuru a')['href']
    etkinlik_title = etkinlik_soup.select_one('#ContentPlaceHolder1_pnl_Duyuru h3').text

    # Duyuru ve etkinlik bilgilerini dosyalara yazıyoruz
    with open('yeni_duyuru.txt', 'w') as f:
        f.write(f"{duyuru_title}\n{duyuru_link}\n")

    with open('yeni_etkinlik.txt', 'w') as f:
        f.write(f"{etkinlik_title}\n{etkinlik_link}\n")

    # Dosyalardaki verileri karşılaştırıyoruz
    with open('eski_duyuru.txt') as f:
        eski_duyuru = f.read()

    with open('eski_etkinlik.txt') as f:
        eski_etkinlik = f.read()

    with open('yeni_duyuru.txt') as f:
        yeni_duyuru = f.read()

    with open('yeni_etkinlik.txt') as f:
        yeni_etkinlik = f.read()

    # Eğer dosyalardaki veriler değişmişse, telegram kanalına mesaj gönderiyoruz
    if eski_duyuru != yeni_duyuru:
        bot.send_message(channel_id, f"📌 DUYURU: {duyuru_title}\n\n🔗 LİNK: https://kapadokya.edu.tr{duyuru_link}")
        print(f"Yeni bir DUYURU bulundu: {duyuru_title}")

    if eski_etkinlik != yeni_etkinlik:
        bot.send_message(channel_id, f"📌 ETKİNLİK: {etkinlik_title}\n\n🔗 LİNK: https://kapadokya.edu.tr{etkinlik_link}")
        print(f"Yeni bir ETKİNLİK: bulundu: {etkinlik_title}")

    else:
        print(f"Yeni bir duyuru veya etkinlik bulunmamaktadır. Saat: {time.strftime('%X')}")

    # Dosyalardaki verileri eşitliyoruz
    with open('eski_duyuru.txt', 'w') as f:
        f.write(yeni_duyuru)

    with open('eski_etkinlik.txt', 'w') as f:
        f.write(yeni_etkinlik)

    # 30 saniyede bir döngüyü tekrarlıyoruz

    time.sleep(3600)

