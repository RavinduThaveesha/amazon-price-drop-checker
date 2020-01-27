import requests
from bs4 import BeautifulSoup
import smtplib 

class PriceChecker:
    def __init__(self, url, email, password, price):
        self.url = url
        self.email = email
        self.password = password
        self.price = price

    def checkPrice(self):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')

        price = soup.find(id="priceblock_ourprice").get_text()
        convertedPrice = float(price[1:4])

        if (convertedPrice < self.price):
            self.sendMail()
        
    def sendMail(self): 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(self.email, self.password)
        subject = 'Price fell down'
        body = 'check the amazon link ' + self.url

        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            self.email,
            self.email,
            message
        )

        print('Email Sent')
        server.quit()

cp = PriceChecker(
    'URL',
    'EMAIL',
    'EMAIL PASSWORD',
    300
)
cp.checkPrice()