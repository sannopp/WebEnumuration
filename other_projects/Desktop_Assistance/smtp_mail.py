import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def send_email(mail_to, sub):
    # edit later enter credentials
    # for mail content(body) goto D:/samples/ and edit the file named mail_content-smtp-mail-python.txt
    my_mail = 'test.mail.screept@gmail.com'
    with open("D:/samples/password-smtp-mail-python.txt", 'r') as f:
        my_password = f.read()

    # my_password = ''
    msg = MIMEMultipart()
    msg['From'] = "AFTAB SAMA"
    msg['To'] = mail_to
    msg['Subject'] = sub

    with open("D:/samples/mail_content-smtp-mail-python.txt", 'r') as f:
        message = f.read()

    msg.attach(MIMEText(message, 'Plain'))

    # filename = "pirates.jpg"          # name of the attached file
    # filename_path = "D:/samples/wp5186473.jpg"
    # attachment = open(filename_path, 'rb')
    #
    # p = MIMEBase('application', 'octet-stream')
    # p.set_payload(attachment.read())
    #
    # encoders.encode_base64(p)
    # p.add_header('Content-Disposition', f'attachment; filename={filename}')
    # msg.attach(p)

    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()

    server.starttls()

    server.ehlo()
    server.login(my_mail, my_password)

    server.sendmail(my_mail, mail_to, text)
    print(f"mail sent successfully \nFrom:{my_mail}\nTo: {mail_to}")


if __name__ == '__main__':
    # edit later enter credentials
    # my_mail = 'test.mail.screept@gmail.com'
    email_to = 'test.mail.screept@gmail.com'  # receiver's mail
    e_sub = 'Subject of mail'  # Subject of mail

    send_email(email_to, e_sub)
