# -*- coding: utf-8 -*-
#
# wat-bridge
# https://github.com/rmed/wat-bridge
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Rafael Medina García <rafamedgar@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Helper functions."""

from wat_bridge.static import DB, CONTACT

def get_contact(phone):
    """Get contact name from a phone number.

    Args:
        phone (str): Phone to search

    Returns:
        String with the contact name or `None` if not found.
    """
    result = DB.get((CONTACT.phone == phone) & (CONTACT.blacklisted == False))

    if not result:
        return None

    return result['name']

def get_phone(contact):
    """Get phone number from a contact name.

    Args:
        contact (str): Name assigned to the contact

    Returns:
        String with the phone number or `None` if not found.
    """
    result = DB.get((CONTACT.name == contact) & (CONTACT.blacklisted == False))

    if not result:
        return None

    return result['phone']

def is_blacklisted(phone):
    """Check if a phone number is blacklisted.

    Args:
        phone (str): Phone to check

    Returns:
        True or False
    """
    result = DB.get((CONTACT.phone == phone) & (CONTACT.blacklisted == True))

    if not result:
        return False

    return True
