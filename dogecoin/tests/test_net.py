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

import unittest

from dogecoin.net import CAddress

class Test_CAddress(unittest.TestCase):
    def test_serializationSimple(self):
        c = CAddress()
        cSerialized = c.serialize()
        cDeserialized = CAddress.deserialize(cSerialized)
        cSerializedTwice = cDeserialized.serialize()
        self.assertEqual(cSerialized, cSerializedTwice)

    def test_serializationIPv4(self):
        c = CAddress()
        c.ip = "1.1.1.1"
        c.port = 8333
        c.nTime = 1420576401

        cSerialized = c.serialize()
        cDeserialized = CAddress.deserialize(cSerialized)
        
        self.assertEqual(c, cDeserialized)
        
        cSerializedTwice = cDeserialized.serialize()
        self.assertEqual(cSerialized, cSerializedTwice)


    def test_serializationIPv6(self):
        c = CAddress()
        c.ip = "1234:ABCD:1234:ABCD:1234:00:ABCD:1234"
        c.port = 8333
        c.nTime = 1420576401

        cSerialized = c.serialize()
        cDeserialized = CAddress.deserialize(cSerialized)
        
        self.assertEqual(c, cDeserialized)
        
        cSerializedTwice = cDeserialized.serialize()
        self.assertEqual(cSerialized, cSerializedTwice)


    def test_serializationDiff(self):
        # Sanity check that the serialization code preserves differences
        c1 = CAddress()
        c1.ip = "1.1.1.1"
        c1.port = 8333
        c1.nTime = 1420576401

        c2 = CAddress()
        c2.ip = "1.1.1.2"
        c2.port = 8333
        c2.nTime = 1420576401

        self.assertNotEqual(c1, c2)

        c1Serialized = c1.serialize()
        c2Serialized = c2.serialize()

        self.assertNotEqual(c1Serialized, c2Serialized)

        c1Deserialized = CAddress.deserialize(c1Serialized)
        c2Deserialized = CAddress.deserialize(c2Serialized)

        self.assertNotEqual(c1Deserialized, c2Deserialized)
