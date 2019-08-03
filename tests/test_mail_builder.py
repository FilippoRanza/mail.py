#! /usr/bin/python

"""
test various configuration for
mail_sender_factory
"""

import unittest

from tempfile import NamedTemporaryFile
from secrets import choice
from string import ascii_letters
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from mail_sender import message_builder



def rand_string():
    """
    build a random, sized length, subject
    """
    out = ''
    for _ in range(24):
        out += choice(ascii_letters)
    return out


class TestMessageBuilder(unittest.TestCase):
    """
    a lonely test case
    """


    def test_with_attachment(self):
        """
        test a correct behavior when only
        an attachment is available
        """
        with NamedTemporaryFile() as file:
            subj = rand_string()
            mail = message_builder('tests/test_conf.json', file.name, subj, None)
            self.assertEqual(mail.mail['Subject'], subj)
            self.assertIsInstance(mail.mail.get_payload(0), MIMEApplication)


    def test_with_file(self):
        """
        test a correct behavior when only
        a message file is available
        """
        with NamedTemporaryFile() as file:
            subj = rand_string()
            mail = message_builder('tests/test_conf.json', None, subj, file.name)
            self.assertEqual(mail.mail['Subject'], subj)
            self.assertIsInstance(mail.mail.get_payload(0), MIMEText)


    def test_with_file_and_attachment(self):
        """
        test a correct behavior when both
        a message file and an attachment are available
        """
        with NamedTemporaryFile() as file:
            subj = rand_string()
            mail = message_builder('tests/test_conf.json', file.name, subj, file.name)
            self.assertEqual(mail.mail['Subject'], subj)

            # attachment, when available are always the first thing added
            self.assertIsInstance(mail.mail.get_payload(0), MIMEApplication)
            self.assertIsInstance(mail.mail.get_payload(1), MIMEText)

if __name__ == "__main__":
    unittest.main()
