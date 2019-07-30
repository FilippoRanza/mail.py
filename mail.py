#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import sys

import smtplib
import json

from os import path

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.message import EmailMessage

from argparse import ArgumentParser

DEFAULT_SUBJECT = "A message from mail.py"
DEFAULT_CONFIG_FILE = "/etc/mail_config.json"


class MailSender:

    def __init__(self, user, passwd, server, port):
        self.user = user
        self.passwd = passwd
        self.server = server
        self.port = port
        self.mail = None

    def __build_mail__(self, subj):
        if self.mail:
            return

        mail = MIMEMultipart()

        mail['Subject'] = subj
        mail['from'] = self.user

        self.mail = mail

    def make_mail(self, msg, subj):
        self.__build_mail__(subj)
        text = MIMEText(msg, 'plain')
        self.mail.attach(text)

    def make_attachment(self, file, subj):
        self.__build_mail__(subj)

        with open(file, "rb") as f_in:
            attach = MIMEApplication(f_in.read(),
                                     Name=path.basename(file))

        attach['Content-Disposition'] = 'attachment; filename="%s"' % path.basename(file)
        self.mail.attach(attach)

    def send_mail(self, dest):
        server = smtplib.SMTP(self.server, port=self.port)
        server.starttls()
        server.login(self.user, self.passwd)
        server.send_message(self.mail, to_addrs=dest)
        server.quit()


def load_config(conf_file):
    with open(conf_file) as f_in:
        try:
            out = json.load(f_in)
        except json.JSONDecodeError:
            out = None
    return out


def mail_sender_factory(conf_file):
    conf = load_config(conf_file)
    if conf:
        try:
            out = MailSender(**conf)
        except:
            raise ValueError('Configuration Error')
    else:
        raise TypeError('Error in Configuration File')
    return out


def load_file(file_name):
    if file_name:
        with open(file_name) as f_in:
            out = f_in.read()
    else:
        out = sys.stdin.read()

    return out


def parse_destination_file(file):
    with open(file) as f_in:
        for line in f_in.readlines():
            if not line:
                continue

            out = line.split()
            for i in out:
                yield i


def load_destination(dest):
    out = []
    for dst in dest:
        if path.isfile(dst):
            for d in parse_destination_file(dst):
                out.append(d)
        else:
            out.append(dst)
    return out


def message_builder(args):
    mail = mail_sender_factory(args.config)
    attach = False
    if args.attachment:
        mail.make_attachment(args.attachment, args.subject)
        attach = True
  
    if args.file or (not attach):
        msg = load_file(args.file)
        mail.make_mail(msg, args.subject)

    return mail




def setup_argparser():
    out = ArgumentParser()
    out.add_argument('-d', '--destination', required=True, nargs='+',
                     help='''Set destination addresse[es], this argument
                     can be a file in this case adress[es] are read from it,
                     addresses are line or spece separated''')
    out.add_argument('-s', '--subject', default=DEFAULT_SUBJECT,
                     help='specify subject')
    out.add_argument('-c', '--config', default=DEFAULT_CONFIG_FILE,
                     help='specify configuration file')
    out.add_argument('-a', '--attachment', default=None,
                     help='add attachment file, just one')
    out.add_argument('-f', '--file',
                     help="specify message file")

    return out


def main():
    parser = setup_argparser()
    args = parser.parse_args()
    if args:
        mail = message_builder(args)
        dst = load_destination(args.destination)
        mail.send_mail(dst)


if __name__ == "__main__":
    main()
