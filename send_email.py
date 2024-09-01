import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from pretty_html_table import build_table


class Email:
    def __init__(self,file,subject:str,sender_email,sender_pw,to_email) -> None:
        
        self.data = pd.read_csv(file)
        self.subject = subject
        self.sender_email = sender_email
        self.to_email = to_email
        
        self.server = smtplib.SMTP("smtp.gmail.com",587)
        self.server.starttls()
        self.server.login(sender_email,sender_pw)
        
        self.message = MIMEMultipart()
    
    def send_out(self):      
        self.message['Subject'] = self.subject 
        self.message['From'] = self.sender_email
        self.message['To'] = self.to_email
        output = build_table(self.data,"blue_light")
        self.message.attach(MIMEText(output, "html"))
        msg_body = self.message.as_string()

        self.server.sendmail(self.sender_email,self.to_email,msg_body)
        print("Email has been sent to " + self.to_email)