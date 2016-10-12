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

"""Listener functions."""

import time

from wat_bridge.static import get_logger
from wat_bridge.tg import tgbot
from wat_bridge.wa import WA_STACK, _connect_signal

logger = get_logger('listeners')

def tg_listener():
    """Poll for new messages in Telegram."""
    while True:
        try:
            # Continue even after an exception occurs
            logger.info('Start Telegram polling')
            tgbot.polling(none_stop=True)

        except Exception as e:
            logger.error(e)

            logger.info('Start Telegram sleep')
            time.sleep(10)
            logger.info('Ended Telegram sleep')

            pass

        # Stop polling and restart it in next iteration
        logger.info('Stop polling')
        tgbot.stop_polling()

def wa_listener():
    """Poll for new messages in Whatsapp."""
    while True:
        try:
            # Continue even after an exception occurs
            logger.info('Start Whatsapp polling')

            WA_STACK.broadcastEvent(_connect_signal)
            WA_STACK.loop()

        except Exception as e:
            logger.error(e)

            logger.info('Start Whatsapp sleep')
            time.sleep(10)
            logger.info('Ended Whatsapp sleep')

            pass
