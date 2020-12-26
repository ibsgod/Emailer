import smtplib
import time
from email.mime.text import MIMEText
import email
import imaplib

def send(to, yes):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    username = 'EMAIL_HERE'
    password = 'PASSWORD_HERE'

    from_addr = username
    to_addrs = [to]
    if yes == 2:
        message = MIMEText("How did you know?! You must truly be the saviour of Christmas and for that I will give you the second part of the key: _fala1alA1AAAA")
        message['subject'] = 'HOHOHO'
    elif yes == 1:
        message = MIMEText("I'm afraid I can't just give you the key, stranger. Like do you even know my favourite food? How can I trust you?")
        message['subject'] = 'Nonono....'
    else:
        message = MIMEText("Do I know you? Do you need something? Don't be shy!")
        message['subject'] = 'Hohowho?....'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    print("Sent email", yes, "to:", to)
    server.quit()

EMAIL = 'merrycodemas@gmail.com'
PASSWORD = 'chadam12345'
SERVER = 'imap.gmail.com'
oldmail = []
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')
status, data = mail.search(None, 'ALL')
mail_ids = []
for block in data:
    mail_ids += block.split()

for i in mail_ids:
    status, data = mail.fetch(i, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])
            mail_from = message['from']
            mail_subject = message['subject']
            if message.is_multipart():
                mail_content = ''
                for part in message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                mail_content = message.get_payload()
            oldmail.append(i)
            break
z = 1
while True:
    if z % 600:
        mail = imaplib.IMAP4_SSL(SERVER)
        mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []
    for block in data:
        mail_ids += block.split()
    for i in mail_ids:
        if i in oldmail:
            continue
        oldmail.append(i)
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()
                print("Received email from:", mail_from)
                if "chicken nuggets" in mail_content.lower() + mail_subject.lower():
                    send(mail_from, 2)
                    break
                print(mail_subject)
                print(mail_content)
                if "key" in mail_content.lower() + mail_subject.lower():
                        send(mail_from, 1)
                else:
                    send(mail_from, 0)
                break
    time.sleep(1)
    z += 1