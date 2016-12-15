import smtplib
from email.mime.text import MIMEText

#update these variables as needed

mailServer = "netservices3.lab.tenablesecurity.com"
mailPort = 25


#alert class. Doesn't take any arguments when being created. 

class Alert:
    
    def __init__(self):
        self.recipient = ""
        self.sender = ""
        self.message = ""
        self.subject = ""
        
    def updateSubject(self,subject):
        self.subject = subject
        
    def updateRecipient(self,name):
        self.recipient = name
        
    def updateSender(self,name):
        self.sender = name
        
    def updateMessage(self,message):
        self.message = message
        
    def sendEmail(self):
        message = str(self.message)
        msg = MIMEText(message,'plain')
        msg['Subject'] = self.subject
        me = self.recipient
        msg['From'] = me
        msg['To'] = me
        
        try:
            s = smtplib.SMTP(mailServer,mailPort)
            s.send_message(msg)
        except Exception as e:
            print(e)
            print("email was not sent")
