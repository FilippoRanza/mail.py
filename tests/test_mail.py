#! /usr/bin/python3

"""
test for mail.py
"""


import unittest
import json
import tempfile

from mail_sender.load_destination import load_destination
from mail_sender.mail_sender import mail_sender_factory, MailSender


class TestLoadDestination(unittest.TestCase):
    """
    test load_destination
    """

    def test_load_destination(self):
        """
        test load_destination
        """

        # this list is like the one coming from arg parser
        arg = ['address@email.com', 'addresses_example.txt', 'mail@mail.com']
        correct = ['address@email.com',
                   'example@test.com',
                   'test@example.com',
                   'mail@service.com',
                   'user@mail.com',
                   'mail@mail.com']
        # this value is a list when used in mail.py
        ans = load_destination(arg)

        self.assertEqual(correct, ans)



class TestMailSenderFactory(unittest.TestCase):
    """
    test for mail_sender_factory
    """

    def test_correct(self):
        """
        this test is run in ideal condition,
        this code should generate a correct
        MailSender
        """
 
        mail = mail_sender_factory('tests/test_conf.json')
        self.assertIsInstance(mail, MailSender)
        
        # values from test_conf.json
        self.assertEqual('example@email.com', mail.user)
        self.assertEqual('example_password', mail.passwd)
        self.assertEqual('smtp.email.com', mail.server)
        self.assertEqual(123, mail.port)





    def test_wrong_config(self):
        """
        test when the configuration file
        exists and it actually contains some
        correct json, but it is not a correct
        configuration because of a
        misspelled key word
        """

        with self.assertRaises(ValueError):
            mail_sender_factory('tests/misspelled_conf.json')





    def test_syntax_error_config(self):
        """
        test when the configuration file
        exists but it doesn't contain any
        correct json
        """
        with self.assertRaises(TypeError):
             mail_sender_factory('tests/wrong_conf.json')



if __name__ == "__main__":
    unittest.main()
