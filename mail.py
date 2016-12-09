import smtplib
from email.mime.text import MIMEText

#alert class. Doesn't take any arguments when being created. 

class Alert:

    def __init__(self):
        self.recipient = ""
        self.sender = ""
        self.message = ""
        
    def updateRecipient(self,name):
        self.recipient = name

    def updateSender(self,name):
        self.sender = name

    def updateMessage(self,message):
        self.message = message

    def sendEmail(self):
        message = str(self.message)
        msg = MIMEText(message,'plain')
        msg['Subject'] = "scan starting soon"
        me = self.recipient
        msg['From'] = me
        msg['To'] = me

        try:
            s = smtplib.SMTP(' ',25)
            s.send_message(msg)
            print("email sent")
        except Exception as e:
            print(e)
            print("email was not sent")


#leaving this in as a test for right now
#newEmail = Alert()
#newEmail.updateRecipient("nroy@tenable.com")
#newEmail.sendEmail()

