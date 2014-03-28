#/usr/bin/env python
#coding:utf-8

from validator import is_valid_bytes_string
import unittest

class IsValidBytesString(unittest.TestCase):
    def test_1(self):
        self.assertFalse(is_valid_bytes_string("0"))
    def test_2(self):
        self.assertFalse(is_valid_bytes_string("0x"))
    def test_3(self):
        self.assertFalse(is_valid_bytes_string("0x8"))
    def test_4(self):
        self.assertTrue(is_valid_bytes_string("0x80"))
    def test_5(self):
        self.assertFalse(is_valid_bytes_string("0x800"))

    def test_first_1(self):
        self.assertFalse(is_valid_bytes_string("0a00"))
    def test_first_2(self):
        self.assertTrue(is_valid_bytes_string("0x80"))

    def test_hex_00(self):
        self.assertTrue(is_valid_bytes_string("0x00"))
    def test_hex_aa(self):
        self.assertTrue(is_valid_bytes_string("0xaa"))
    def test_hex_Aa(self):
        self.assertTrue(is_valid_bytes_string("0xAa"))
    def test_hex_AA(self):
        self.assertTrue(is_valid_bytes_string("0xAA"))
    def test_hex_N0(self):
        self.assertFalse(is_valid_bytes_string("0xN0"))
    def test_hex_0N(self):
        self.assertFalse(is_valid_bytes_string("0x0N"))

if __name__ == "__main__":
    unittest.main()

