import time
from Email_cred import email,pw
from send_email import Email

file = "/home/baichen/ibkr_daily_pnl/" + time.strftime("%d_%m_%Y") + "_DailyPnL.csv"
subject = time.strftime("%d-%m-%Y") + ' Daily Profit and Loss Report!'

email = Email(file,subject,email,pw,email)
email.send_out()
