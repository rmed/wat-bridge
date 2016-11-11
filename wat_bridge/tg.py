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

"""Code for the Telegram side of the bridge."""

import telebot

from wat_bridge.static import SETTINGS, SIGNAL_WA, get_logger
from wat_bridge.helper import db_add_contact, db_rm_contact, \
        db_add_blacklist, db_rm_blacklist, db_list_contacts, \
        get_blacklist, get_contact, get_phone, is_blacklisted, \
        db_get_group, db_set_group, db_get_contact_by_group, safe_cast

logger = get_logger('tg')

# Telegram bot
tgbot = telebot.TeleBot(
    SETTINGS['tg_token'],
    threaded=False,
    skip_pending=False
)

# Create handlers

@tgbot.message_handler(commands=['start', 'help'])
def start(message):
    """Show usage of the bot.

    Args:
        message: Received Telegram message.
    """
    response = ('wat-bridge\n\n'
                'Usage:\n\n'
                '   /help -> shows this help message\n'
                '   /add <name> <phone> -> add a new contact to database\n'
                '   /bind <name> <group id> -> bind a contact to a group\n'
                '   /contacts -> list contacts\n'
                '   /blacklist -> show blacklisted Whatsapp phones\n'
                '   /blacklist <phone> -> blacklist a phone number\n'
                '   /rm <name> -> remove a contact from database\n'
                '   /send <name> <message> -> send message to Whatsapp contact\n'
                '   /unbind <name> -> unbind a contact from his group\n'
                '   /unblacklist <phone> -> unblacklist a phone number\n\n'
                'Note that blacklisting a phone number will make the bot ignore'
                ' any Whatsapp messages that come from that number.'
               )

    tgbot.reply_to(message, response)

@tgbot.message_handler(commands=['me'])
def me(message):
    """Get user ID.

    Args:
        message: Received Telegram message.
    """
    tgbot.reply_to(message, message.chat.id)

@tgbot.message_handler(commands=['add'])
def add_contact(message):
    """Add a new Whatsapp contact to the database.

    Message has the following format:

        /add <name> <phone>

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'You are not the owner of this bot')
        return

    # Get name and phone
    args = telebot.util.extract_arguments(message.text)
    name, phone = args.split(maxsplit=1)

    if not name or not phone:
        tgbot.reply_to(message, 'Syntax: /add <name> <phone>')
        return

    # Check if it already exists
    if get_contact(phone) or get_phone(name):
        tgbot.reply_to(message, 'A contact with those details already exists')
        return

    # Add to database
    db_add_contact(name, phone)

    tgbot.reply_to(message, 'Contact added')

@tgbot.message_handler(commands=['bind'])
def bind(message):
    """Bind a contact to a group.

    Message has the following format:

        /bind <name> <group id>

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'You are not the owner of this bot')
        return

    # Get name and phone
    args = telebot.util.extract_arguments(message.text)
    name, group_id = args.split(maxsplit=1)

    if not name or not group_id:
        tgbot.reply_to(message, 'Syntax: /bind <name> <group id>')
        return

    group_id = safe_cast(group_id, int)
    if not group_id:
        tgbot.reply_to(message, 'Group id has to be a number')
        return

    # Ensure contact exists
    if not get_phone(name):
        tgbot.reply_to(message, 'No contact found with that name')
        return

    # Check if it already exists
    current = db_get_contact_by_group(group_id)
    if current:
        tgbot.reply_to(message, 'This group is already bound to ' + current)
        return

    # Add to database
    db_set_group(name, group_id)

    tgbot.reply_to(message, 'Bound to group')

@tgbot.message_handler(commands=['unbind'])
def unbind(message):
    """Unbind a contact from his group.

    Message has the following format:

        /unbind <name>

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'You are not the owner of this bot')
        return

    # Get name and phone
    name = telebot.util.extract_arguments(message.text)

    if not name:
        tgbot.reply_to(message, 'Syntax: /unbind <name>')
        return

    # Ensure contact exists
    if not get_phone(name):
        tgbot.reply_to(message, 'No contact found with that name')
        return

    # Check if it already exists
    group = db_get_group(name)
    if not group:
        tgbot.reply_to(message, 'Contact was not bound to a group')
        return

    # Add to database
    db_set_group(name, None)

    tgbot.reply_to(message, 'Unbound from group')

@tgbot.message_handler(commands=['blacklist'])
def blacklist(message):
    """Blacklist a Whatsapp phone.

    Message has the following format:

        /blacklist
        /blacklist <phone>

    Note that if no phone is provided, a list of blacklisted phone is returned.

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'you are not the owner of this bot')
        return

    # Get phone
    phone = telebot.util.extract_arguments(message.text)

    if not phone:
        # Return list
        blacklist = get_blacklist()

        response = 'Blacklisted phones:\n\n'
        for b in blacklist:
            response += '- %s\n' % b

        tgbot.reply_to(message, response)
        return

    # Blacklist a phone
    if is_blacklisted(phone):
        # Already blacklisted
        tgbot.reply_to(message, 'That phone is already blacklisted')
        return

    db_add_blacklist(phone)

    tgbot.reply_to(message, 'Phone has been blacklisted')

@tgbot.message_handler(commands=['contacts'])
def list_contacts(message):
    """List stored contacts.

    Message has the following format:

        /contacts

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'you are not the owner of this bot')
        return

    contacts = db_list_contacts()

    response = 'Contacts:\n'
    for c in contacts:
        response += '- %s (%s)' % (c[0], c[1])
        if c[2]:
            response += ' -> group %s' % c[2]
        response += '\n'

    tgbot.reply_to(message, response)

@tgbot.message_handler(commands=['rm'])
def rm_contact(message):
    """Remove a Whatsapp contact from the database.

    Message has the following format:

        /rm <name>

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'you are not the owner of this bot')
        return

    # Get name
    name = telebot.util.extract_arguments(message.text)

    if not name:
        tgbot.reply_to(message, 'Syntax: /rm <name>')
        return

    # Check if it already exists
    if not get_phone(name):
        tgbot.reply_to(message, 'No contact found with that name')
        return

    # Add to database
    db_rm_contact(name)

    tgbot.reply_to(message, 'Contact removed')

@tgbot.message_handler(commands=['send'])
def relay_wa(message):
    """Send a message to a contact through Whatsapp.

    Message has the following format:

        /send <name> <message>

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'you are not the owner of this bot')
        return

    # Get name and message
    args = telebot.util.extract_arguments(message.text)
    name, text = args.split(maxsplit=1)

    if not name or not text:
        tgbot.reply_to(message, 'Syntax: /send <name> <message>')
        return

    # Relay
    logger.info('relaying message to Whatsapp')
    SIGNAL_WA.send('tgbot', contact=name, message=text)

@tgbot.message_handler(commands=['unblacklist'])
def unblacklist(message):
    """Unblacklist a Whatsapp phone.

    Message has the following format:

        /unblacklist <phone>

    Args:
        message: Received Telegram message.
    """
    if message.chat.id != SETTINGS['owner']:
        tgbot.reply_to(message, 'you are not the owner of this bot')
        return

    # Get phone
    phone = telebot.util.extract_arguments(message.text)

    if not phone:
        # Return list
        tgbot.reply_to(message, 'Syntax: /unblacklist <phone>')
        return

    # Unblacklist a phone
    if not is_blacklisted(phone):
        # Not blacklisted
        tgbot.reply_to(message, 'That phone is not blacklisted')
        return

    db_rm_blacklist(phone)

    tgbot.reply_to(message, 'Phone has been unblacklisted')

@tgbot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def relay_group_wa(message):
    """ Send a message received in a bound group to the correspondending contact through Whatsapp.

    Args:
        message: Received Telegram message.
    """
    cid = message.chat.id
    uid = message.from_user.id

    if uid != SETTINGS['owner']:
        tgbot.reply_to(message, 'you are not the owner of this bot')
        return

    name = db_get_contact_by_group(group=cid)
    if not name:
        tgbot.reply_to(message, 'no user is mapped to this group')
        return

    # Relay
    logger.info('relaying message to Whatsapp')
    SIGNAL_WA.send('tgbot', contact=name, message=message.text)
