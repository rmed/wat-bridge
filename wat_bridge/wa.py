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

"""Code for the Whatsapp side of the bridge."""

from yowsup.layers import YowLayerEvent
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.stacks import YowStackBuilder

from wat_bridge.static import SETTINGS, SIGNAL_TG, get_logger
from wat_bridge.helper import is_blacklisted

logger = get_logger('wa')

class WaLayer(YowInterfaceLayer):
    """Defines the yowsup layer for interacting with Whatsapp."""

    @ProtocolEntityCallback('message')
    def on_message(self, message):
        """Received a message."""
        # Parse information
        sender = message.getFrom(full=False)

        logger.debug('received message from %s' % sender)

        # Send receipt
        receipt = OutgoingReceiptProtocolEntity(
            message.getId(),
            message.getFrom(),
            'read',
            message.getParticipant()
        )

        self.toLower(receipt)

        # Ignore non-text messages
        if message.getType() != 'text':
            logger.info('not a text message, ignoring')
            return

        # Do stuff
        if is_blacklisted(sender):
            logger.debug('phone is blacklisted: %s' % sender)
            return

        body = message.getBody()

        # Relay to Telegram
        logger.info('relaying message to Telegram')
        SIGNAL_TG.send('wabot', phone=sender, message=body)

    @ProtocolEntityCallback('receipt')
    def on_receipt(self, entity):
        """Received a "receipt" for a message."""
        logger.debug('ACK message')

        # Acknowledge
        ack = OutgoingAckProtocolEntity(
            entity.getId(),
            'receipt',
            entity.getType(),
            entity.getFrom()
        )

        self.toLower(ack)

    def send_msg(self, **kwargs):
        """Send a message.

        Arguments:
            phone (str): Phone to send the message to.
            message (str): Message to send
        """
        phone = kwargs.get('phone')

        if not phone:
            # Nothing to do
            logger.debug('no phone provided')
            return

        message = kwargs.get('message')

        entity = TextMessageProtocolEntity(
            message,
            to='%s@s.whatsapp.net' % phone
        )

        # self.ackQueue.append(entity.getId())
        self.toLower(entity)


# Prepare stack
wabot = WaLayer()

_connect_signal = YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT)

WA_STACK = (
    YowStackBuilder()
    .pushDefaultLayers(True)
    # .pushDefaultLayers(False)
    .push(wabot)
    .build()
)

WA_STACK.setCredentials((SETTINGS['wa_phone'], SETTINGS['wa_password']))
