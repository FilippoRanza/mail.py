#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


"""
This script contains MailSender a wrapper around
python's email and smtp implementation and it's
factory function
"""

import json
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class MailSender:

    def __init__(self, user, passwd, server, port):
        self.user = user
        self.passwd = passwd
        self.server = server
        self.port = port
        self.mail = None

    def __build_mail__(self):
        if self.mail:
            return

        mail = MIMEMultipart()
        mail['from'] = self.user
        self.mail = mail

    def make_mail(self, msg):
        self.__build_mail__()
        text = MIMEText(msg, 'plain')
        self.mail.attach(text)

    def make_attachment(self, data, name):
        self.__build_mail__()
        attach = MIMEApplication(data, Name=name)
        attach['Content-Disposition'] = 'attachment; filename="%s"' % name
        self.mail.attach(attach)

    def set_subject(self, subj):
        self.__build_mail__()
        self.mail['Subject'] = subj

    def send_mail(self, dest):
        server = smtplib.SMTP(self.server, port=self.port)
        server.starttls()
        server.login(self.user, self.passwd)
        server.send_message(self.mail, to_addrs=dest)
        server.quit()


def load_config_file(conf_file):
    with open(conf_file) as f_in:
        try:
            out = json.load(f_in)
        except json.JSONDecodeError:
            out = None
    return out


def mail_sender_factory(conf_file):
    conf = load_config_file(conf_file)
    if conf:
        try:
            out = MailSender(**conf)
        except:
            raise ValueError('Configuration Error')
    else:
        raise TypeError('Error in Configuration File')
    return out
