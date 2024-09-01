import time
from Email_cred import email,pw
from send_email import Email

file = "/home/baichen/watchlist/" + time.strftime("%d_%m_%Y") + "_watchlist.csv"
subject = time.strftime("%d-%m-%Y") + ' watch list!'

email = Email(file,subject,email,pw,email)
email.send_out()