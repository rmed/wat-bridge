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

"""Static elements."""

from six.moves import configparser
from tinydb import TinyDB, Query
from tinydb_smartcache import SmartCacheTable
import blinker
import logging
import os
import sys

# Main settings
SETTINGS = {}

# Database
DB = None
CONTACT = Query()

# Signals
SIGNAL_TG = blinker.signal('TO_TG')
SIGNAL_WA = blinker.signal('TO_WA')

def get_logger(name):
    """ Get a logger with the given name. """
    # Base logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Handler to stdout
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Formatting
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s[%(funcName)s]: %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def init_bridge():
    """Parse the configuration file and set relevant variables."""
    conf_path = os.path.abspath(os.getenv('WAT_CONF', ''))

    if not conf_path or not os.path.isfile(conf_path):
        sys.exit('Could not find configuration file')

    parser = configparser.ConfigParser()
    parser.read(conf_path)

    # Whatsapp settings
    SETTINGS['wa_phone'] = parser.get('wa', 'phone')
    SETTINGS['wa_password'] = parser.get('wa', 'password')

    # Telegram settings
    SETTINGS['owner'] = parser.getint('tg', 'owner')
    SETTINGS['tg_token'] = parser.get('tg', 'token')

    # TinyDB
    global DB
    DB = TinyDB(parser.get('db', 'path'))
    DB.table_class = SmartCacheTable
