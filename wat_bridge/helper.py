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

def db_add_blacklist(phone):
    """Add a new blacklisted phone to the database.

    Args:
        phone (str): Phone of the contact.

    Returns:
        ID of the inserted element.
    """
    return DB.insert({'name': None, 'phone': phone, 'blacklisted': True, 'group': None})

def db_add_contact(name, phone):
    """Add a new contact to the database.

    Args:
        name (str): Name to use for the contact.
        phone (str): Phone of the contact.

    Returns:
        ID of the inserted element.
    """
    return DB.insert({'name': name.lower(), 'phone': phone, 'blacklisted': False, 'group': None})

def db_list_contacts():
    """Obtain a list of contacts.

    The list contains tuples with (name, phone)

    Returns:
        List of tuples
    """
    result = DB.search(CONTACT.blacklisted == False)

    return [(a['name'], a['phone'], a.get('group')) for a in result]

def db_rm_blacklist(phone):
    """Removes a blacklisted phone from the database.

    Args:
        phone (str): Phone of the contact.
    """
    DB.remove((CONTACT.phone == phone) & (CONTACT.blacklisted == True))

def db_rm_contact(name):
    """Remove a contact from the the database.

    Args:
        name (str): Name of the contact to remove.
    """
    DB.remove(CONTACT.name == name.lower())

def get_blacklist():
    """Obtain a list of blacklisted phones.

    Returns:
        List of strings.
    """
    result = DB.search(CONTACT.blacklisted == True)

    if not result:
        return []

    return [a['phone'] for a in result]

def get_contact(phone):
    """Get contact name from a phone number.

    Args:
        phone (str): Phone to search.

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
    result = DB.get((CONTACT.name == contact.lower()) & (CONTACT.blacklisted == False))

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

def db_get_group(contact):
    result = DB.get((CONTACT.name == contact.lower()))

    if not result:
        return None

    # return None for backward compatibility if there is no group column
    return result.get('group')

def db_set_group(contact, group):
    DB.update({'group': group}, (CONTACT.name == contact.lower()))

def db_get_contact_by_group(group):
    """Get phone number from a group id.

    Args:
        group (int): Group id assigned to the contact.

    Returns:
        String with the phone number or `None` if not found.
    """
    result = DB.get((CONTACT.group == group))

    if not result:
        return None

    return result['name']

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
