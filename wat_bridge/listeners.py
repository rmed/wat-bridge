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

from wat_bridge.static import LOG
from wat_bridge.tg import tgbot
from wat_bridge.wa import wastack, _connect_signal


def tg_listener():
    """Poll for new messages in Telegram."""
    while True:
        try:
            # Continue even after an exception occurs
            LOG.info('Start Telegram polling')
            tgbot.polling(none_stop=True)

        except Exception as e:
            LOG.error(e)

            LOG.info('Start Telegram sleep')
            time.sleep(10)
            LOG.info('Ended Telegram sleep')

            pass

        # Stop polling and restart it in next iteration
        LOG.info('Stop polling')
        tgbot.stop_polling()

def wa_listener():
    """Poll for new messages in Whatsapp."""
    while True:
        try:
            # Continue even after an exception occurs
            LOG.info('Start Whatsapp polling')

            wastack.broadcastEvent(_connect_signal)
            wastack.loop()

        except Exception as e:
            LOG.error(e)

            LOG.info('Start Whatsapp sleep')
            time.sleep(10)
            LOG.info('Ended Whatsapp sleep')

            pass
