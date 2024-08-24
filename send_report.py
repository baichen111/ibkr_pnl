import smtplib,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from pretty_html_table import build_table
from Email_cred import email,pw

data = pd.read_csv("/home/baichen/ibkr_daily_pnl/" + time.strftime("%d_%m_%Y") + "_DailyPnL.csv")

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email,pw)

message = MIMEMultipart()
message['Subject'] = time.strftime("%d-%m-%Y") + ' Daily Profit and Loss Report!'
message['From'] = email
message['To'] = email
output = build_table(data,"blue_light")
message.attach(MIMEText(output, "html"))
msg_body = message.as_string()

server.sendmail(email,email,msg_body)
print("Email has been sent to " + email)