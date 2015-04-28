#!/usr/bin/env python3

# Copyright (C) 2013-2014 The python-dogecoinlib developers
#
# This file is part of python-dogecoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-dogecoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Bip-0070-related functionality

Creates http response objects suitable for use with
dogecoin bip 70 using googles protocol buffers.
"""

import urllib2

# https://github.com/dogecoin/bips/blob/master/bip-0070/paymentrequest.proto
import payments_pb2
o = payments_pb2

import dogecoin
#dogecoin.SelectParams('testnet')
from dogecoin.wallet import CDogecoinAddress
from dogecoin.core.script import CScript
from dogecoin.rpc import Proxy

from time import time

def payment_request():
    """Generates a http PaymentRequest object"""

    bc = Proxy()
    doge = bc.getnewaddress()

#   Setting the 'amount' field to 0 (zero) should prompt the user to enter
#   the amount for us but a bug in dogecoin core qt version 0.9.1 (at time of
#   writing) wrongly informs us that the value is too small and aborts.
#   https://github.com/dogecoin/dogecoin/issues/3095
#   Also there can be no leading 0's (zeros).
    doge_amount = 100000
    serialized_pubkey = doge.to_scriptPubKey()

    pdo = o.PaymentDetails()
    #pdo.network = 'test'
    pdo.outputs.add(amount = doge_amount,script = serialized_pubkey)
    pdo.time = int(time())
    pdo.memo = 'String shown to user before confirming payment'
    pdo.payment_url = 'http://payment_ack.url'

    pro = o.PaymentRequest()
    pro.serialized_payment_details = pdo.SerializeToString()

    sds_pr = pro.SerializeToString()

    open('sds_pr_blob', 'wb').write(sds_pr)
    headers = {'Content-Type': 'application/dogecoin-payment',
               'Accept': 'application/dogecoin-paymentrequest'}
    http_response_object = urllib2.Request('file:sds_pr_blob', None, headers)

    return http_response_object


def payment_ack(serialized_Payment_message):
    """Generates a PaymentACK object, captures client refund address and returns a message"""

    pao = o.PaymentACK()
    pao.payment.ParseFromString(serialized_Payment_message)
    pao.memo = 'String shown to user after payment confirmation'

    refund_address = CDogecoinAddress.from_scriptPubKey(CScript(pao.payment.refund_to[0].script))

    sds_pa = pao.SerializeToString()

    open('sds_pa_blob', 'wb').write(sds_pa)
    headers = {'Content-Type' : 'application/dogecoin-payment', 'Accept' : 'application/dogecoin-paymentack'}
    http_response_object = urllib2.Request('file:sds_pa_blob', None, headers)

    return http_response_object
