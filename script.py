from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from twilio.rest import Client
import smtplib
from email.message import EmailMessage
import time
import os

# Configurações via variáveis de ambiente
URL = 'https://service.berlin.de/terminvereinbarung/termin/day/'
EMAIL_DE = os.getenv('EMAIL_DE')
EMAIL_PARA = os.getenv('EMAIL_PARA')
SENHA_EMAIL = os.getenv('SENHA_EMAIL')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH = os.getenv('TWILIO_AUTH')
TWILIO_NUMERO = os.getenv('TWILIO_NUMERO')
SEU_NUMERO = os.getenv('SEU_NUMERO')

def checar_disponibilidade():
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if "Bitte wählen Sie ein Datum" in soup.text:
            return True
        return False
    finally:
        driver.quit()

def enviar_email():
    msg = EmailMessage()
    msg['Subject'] = '🚨 Vaga para Einbürgerungstest disponível!'
    msg['From'] = EMAIL_DE
    msg['To'] = EMAIL_PARA
    msg.set_content(f'Confira agora: {URL}')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_DE, SENHA_EMAIL)
        smtp.send_message(msg)

def enviar_sms():
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(
        body='🚨 Vaga disponível para o Einbürgerungstest! Confira o site.',
        from_=TWILIO_NUMERO,
        to=SEU_NUMERO
    )

if __name__ == "__main__":
    if checar_disponibilidade():
        enviar_email()
        enviar_sms()
        print("Alerta enviado!")
    else:
        print("Nenhuma vaga disponível.")
