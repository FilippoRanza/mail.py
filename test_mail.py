#! /usr/bin/python3

"""
test for mail.py
"""

import unittest
from mail import load_destination


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


if __name__ == "__main__":
    unittest.main()
