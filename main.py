from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

url = "https://camelcamelcamel.com/product/B0BCWVG3TC"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,la;q=0.8"

}

my_email = os.getenv("MY_EMAIL")
# password from app generator on gmail
password = os.getenv("PASSWORD")
other_email = os.getenv("OTHER_EMAIL")

response = requests.get(url, headers=headers)

# lxml is the parser that beautiful soup uses to parse the html file
soup = BeautifulSoup(response.text, "html.parser")

# get the price of the item from the soup object
price = soup.find(name="span", class_="green").getText().strip()
# remove the $ from the price and replace it with nothing
price_without_currency = price.replace("$", "")
# convert the price to a float
price_as_float = float(price_without_currency)

# get the title of the product from the soup object and strip the white space from the title and 0 index it to get
# the title of the product only and not the other products
product_title = soup.select("div h2 a")[0].getText().strip()

# set the target price for the product to be less than or equal to the target price
target_price = float(20.00)

if price_as_float <= target_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # start transport layer security to secure the connection to the email server
        connection.starttls()
        # login process
        connection.login(user=my_email, password=password)
        # sending the email from one address to the other with message...adding subject and /n to make
        # sure it doesn't go into spam box...encode and decode takes away ascii errors
        connection.sendmail(from_addr=my_email, to_addrs=other_email,
                            msg=f"Subject: Price Drop\n\n{product_title} is now {target_price} or less!\n{url}"
                            .encode("utf-8"))
