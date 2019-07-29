#! /usr/bin/python3

"""
test for mail.py
"""


import unittest
import json
import tempfile

from mail import load_destination, mail_sender_factory, MailSender


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
        correct_conf = {
            'user': 'test@email.com',
            'passwd': 'super_passwd',
            'server': 'smtp.email.com',
            'port': 456
        }

        with tempfile.NamedTemporaryFile(mode="r+") as file:
            json.dump(correct_conf, file)
            file.seek(0)
            mail = mail_sender_factory(file.name)
            self.assertIsInstance(mail, MailSender)




    def test_wrong_config(self):
        """
        test when the configuration file
        exists and it actually contains some
        correct json, but it is not a correct
        configuration
        """
        wrong_conf = {
            'account': 'test@email.com',
            'password': 'super_passwd',
            'server': 'smtp.email.com',
            'port': 456
        }

        with tempfile.NamedTemporaryFile(mode="r+") as file:
            json.dump(wrong_conf, file)
            file.seek(0)
            with self.assertRaises(ValueError):
                mail_sender_factory(file.name)





    def test_syntax_error_config(self):
        """
        test when the configuration file
        exists but it doesn't contain any
        correct json
        """

        with tempfile.NamedTemporaryFile(mode="r+") as file:
            file.write('{"test":"value"')
            file.seek(0)
            with self.assertRaises(TypeError):
                mail_sender_factory(file.name)



if __name__ == "__main__":
    unittest.main()
