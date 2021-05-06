#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import json
import smtplib, ssl
import datetime
import os
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def send_email(old, new):

   port = 465
   smtp_server = "smtp.gmail.com"
   sender_email = "nadia.archylak@gmail.com"
   receiver_email = "nadia.chylak@gmail.com, pierre.mezeray@gmail.com"
   password = EMAIL_PASSWORD

   # Create message
   message = MIMEMultipart()
   message["From"] = sender_email
   message["To"] = receiver_email
   message["Subject"] = "CoronaWatch - READ ME!"
   body = "https://zh.vacme.ch\n\n***********\n*** OLD ***\n***********\n\n" + old +"\n***********\n*** NEW ***\n***********\n\n" + new
   message.attach(MIMEText(body, "plain"))
   text = message.as_string()

   # Log in to server using secure context and send email
   context = ssl.create_default_context()
   with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
       server.login(sender_email, password)
       server.sendmail(sender_email, receiver_email, text)

   return None

#**************************

url = 'https://www.zh.ch/de/gesundheit/coronavirus/coronavirus-impfung.html'
response = requests.get(url)
parsed_html = BeautifulSoup(response.content,'html.parser')
with open("old.txt", "r") as f:
    old = f.read()

try:
    new = parsed_html.find("h2", {"id": "215336037"}).parent.text.replace("  ","")
except:
    new = "Invalid ID."
finally:
    for c in parsed_html.find_all(class_="mdl-teaser__content"):
        new = new + "\n*********\n" + c.text.replace("  ","")

if old != new:
    send_email(old, new)

with open("old.txt", "w") as f:
    f.write(new)
