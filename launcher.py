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

"""Main launcher."""

from __future__ import print_function

import signal
import threading

from wat_bridge.static import SIGNAL_TG, SIGNAL_WA, init_bridge

# Parse config file
init_bridge()

from wat_bridge.listeners import tg_listener, wa_listener
from wat_bridge.signals import sigint_handler, to_tg_handler, to_wa_handler


if __name__ == '__main__':
    # Setup signaling
    signal.signal(signal.SIGINT, sigint_handler)
    print('Press Ctrl+C to exit')

    SIGNAL_TG.connect(to_tg_handler)
    SIGNAL_WA.connect(to_wa_handler)

    # Launch threads and wait for them
    tg_thread = threading.Thread(target=tg_listener)
    wa_thread = threading.Thread(target=wa_listener)

    tg_thread.start()
    wa_thread.start()

    tg_thread.join()
    wa_thread.join()
