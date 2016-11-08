import smtplib, subprocess, sys
from email.mime.text import MIMEText
from_address = "z5555555@unsw.edu.au"
to_address = "chenson.van@gmail.com"
message = "hi there"
msg = MIMEText(message)
msg['Subject'] = "Andrew rocks"
msg['From'] = from_address
msg['To'] = to_address
s = smtplib.SMTP('smtp.cse.unsw.edu.au')
s.sendmail(from_address, [to_address], msg.as_string())
s.quit()
print('fine')