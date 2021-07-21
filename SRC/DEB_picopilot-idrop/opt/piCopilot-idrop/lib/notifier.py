import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

class Alert(object):

    def notify(self, body):
        server = '<YOUR SERVER>'
        sender = '<Email Address of sender>'
        dName = ''
        rName = ''
        recipients = 'Recipient Email(s) <foo@bob.com,hello@foo.com>'
        recipients = [to for to in recipients.split(',')]
        subject = 'idrop Alert'
        body = body
        password = '<>'

        ## Server Details
        s = smtplib.SMTP(server + ':587')
        s.set_debuglevel(1)
        s.starttls()
        s.login(sender, password)
        msg = MIMEText(body)
        msg.set_type('text/html')
        msg['Subject'] = subject
        if not dName:
                dName = sender
        msg['From'] = formataddr((str(Header(dName)), sender))
        msg['To'] = ", ".join(recipients)
        if rName:
                msg['reply-to'] = rName
        s.sendmail(sender, recipients, msg.as_string())
