#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

import sys
from os.path import basename

from .mail_sender import mail_sender_factory


def load_text_file(file_name):
    if file_name:
        with open(file_name) as f_in:
            out = f_in.read()
    else:
        out = sys.stdin.read()

    return out

def load_bin_file(file_name):
    with open(file_name, "rb") as f_in:
        out = f_in.read()

    return out


def message_builder(args):
    mail = mail_sender_factory(args.config)
    attach = False
    if args.attachment:
        data = load_bin_file(args.attachment)
        mail.make_attachment(data, basename(args.attachment), args.subject)
        attach = True

    if args.file or (not attach):
        msg = load_text_file(args.file)
        mail.make_mail(msg, args.subject)

    return mail
