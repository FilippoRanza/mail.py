#! /usr/bin/python3

"""
test for mail.py
"""

from mail import load_destination


def test_load_destination():
    """
    test load_destination
    """
    correct = ['address@email.com',
               'example@test.com',
               'test@example.com',
               'mail@service.com',
               'user@mail.com',
               'mail@mail.com']
    # this value is a list when used in mail.py
    ans = load_destination(['address@email.com', 'addresses_example.txt', 'mail@mail.com'])

    assert correct == ans
