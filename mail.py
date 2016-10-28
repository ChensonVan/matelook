#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Changxun Fan'

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from config_default import configs

import smtplib
from db import next_id

_URL_ = configs['URL']
_PORT_ = configs['PORT']


class MailUtils():
    def __init__(self, to_addr, sender, receiver):
        self.from_addr = 'andersonvan.cn@gmail.com'
        self.password = 'Anderson186.'
        self.to_addr = to_addr
        self.sender = sender
        self.receiver = receiver

    def _format_addr(self, address):
        name, addr = parseaddr(address)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self):
        content = 'hello {}, {} want to add you as friends!'.format(self.receiver, self.sender)
        msg = MIMEText(content)
        msg['From'] = self._format_addr('{} <{}>'.format(self.sender, self.from_addr))
        msg['To'] = self._format_addr('{} <{}>'.format(self.receiver, self.to_addr))
        msg['Subject'] = Header('Password Recovery', 'utf-8').encode()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, self.to_addr, msg.as_string())
        server.close()

    def reset(self, zid, code=next_id()):
        content = 'Please click the url to reset your password.\n\n'
        content += '%s:%s/account/reset?zid=%s&&resetCode=%s' % (_URL_, _PORT_, zid, code)
        # print(content)
        msg = MIMEText(content)
        msg['From'] = self._format_addr('{} <{}>'.format(self.sender, self.from_addr))
        msg['To'] = self._format_addr('{} <{}>'.format(self.receiver, self.to_addr))
        msg['Subject'] = Header('From matelook ... ', 'utf-8').encode()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, self.to_addr, msg.as_string())
        server.close()


if __name__ == '__main__':
    mail = MailUtils('chenson.van@gmail.com', 'changxun', 'vane')
    print('begin')
    # mail.send()
    print('end')
    print(next_id())
    print()
    print(_URL_)
    mail.reset('z5006334')