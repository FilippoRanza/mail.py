#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


from argparse import ArgumentParser
from mail import message_builder, load_destination

DEFAULT_SUBJECT = "A message from mail.py"
DEFAULT_CONFIG_FILE = "/etc/mail_config.json"




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
