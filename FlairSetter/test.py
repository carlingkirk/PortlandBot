import smtplib
gmail_user = 'stephbairey@gmail.com'
gmail_pwd = 'k3Stra123'
FROM = 'stephbairey@gmail.com'
TO = 'scb.zombie@gmail.com'
SUBJECT = 'test subject'
TEXT = 'test body'

message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print ('successfully sent the mail')
except:
    print ("failed to send mail")

message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

try:
    server_ssl = smtplib.SMTP_SSL("smtp.googlemail.com", 465)
    server_ssl.ehlo()
    server_ssl.login(gmail_user, gmail_pwd)
    server_ssl.sendmail(FROM, TO, message)
    server_ssl.close()
    print ('successfully sent the SSL mail')
except:
    print ("failed to send SSL mail")
