#/usr/bin/env python
#coding:utf-8

from validator import *
import unittest

class ValidatorIsValidBytesString(unittest.TestCase):
    def test_1(self):
        self.assertFalse(Validator.is_valid_bytes_string("0"))
    def test_2(self):
        self.assertFalse(Validator.is_valid_bytes_string("0x"))
    def test_3(self):
        self.assertFalse(Validator.is_valid_bytes_string("0x8"))
    def test_4(self):
        self.assertTrue(Validator.is_valid_bytes_string("0x80"))
    def test_5(self):
        self.assertFalse(Validator.is_valid_bytes_string("0x800"))

    def test_first_1(self):
        self.assertFalse(Validator.is_valid_bytes_string("0a00"))
    def test_first_2(self):
        self.assertTrue(Validator.is_valid_bytes_string("0x80"))

    def test_hex_00(self):
        self.assertTrue(Validator.is_valid_bytes_string("0x00"))
    def test_hex_aa(self):
        self.assertTrue(Validator.is_valid_bytes_string("0xaa"))
    def test_hex_Aa(self):
        self.assertTrue(Validator.is_valid_bytes_string("0xAa"))
    def test_hex_AA(self):
        self.assertTrue(Validator.is_valid_bytes_string("0xAA"))
    def test_hex_N0(self):
        self.assertFalse(Validator.is_valid_bytes_string("0xN0"))
    def test_hex_0N(self):
        self.assertFalse(Validator.is_valid_bytes_string("0x0N"))

class ValidatorCheckHeader(unittest.TestCase):
    def test_checkheader_same(self):
        self.assertTrue(Validator.check_header([1,2,3],[1,2,3]))
    def test_checkheader_1(self):
        self.assertTrue(Validator.check_header([1,2,3],[1,2,3,4]))
    def test_checkheader_2(self):
        self.assertFalse(Validator.check_header([1,2,3,4],[1,2,3]))

class ValidatorIsValidUnitString(unittest.TestCase):
    pass

class ValidatorIsValidDataSize(unittest.TestCase):
    def test_decimal1(self):
        self.assertTrue(Validator.is_valid_data_size("0"))
    def test_decimal2(self):
        self.assertTrue(Validator.is_valid_data_size("10"))
    def test_real(self):
        self.assertFalse(Validator.is_valid_data_size("1.0"))
    def test_hex1(self):
        self.assertFalse(Validator.is_valid_data_size("A"))
    def test_hex2(self):
        self.assertFalse(Validator.is_valid_data_size("0A"))
    def test_max1(self):
        self.assertFalse(Validator.is_valid_data_size("<="))
    def test_max2(self):
        self.assertTrue(Validator.is_valid_data_size("<= 1"))
    def test_max3(self):
        self.assertFalse(Validator.is_valid_data_size("<= 1 2"))
    def test_or1(self):
        self.assertFalse(Validator.is_valid_data_size("or"))
    def test_or2(self):
        self.assertFalse(Validator.is_valid_data_size("or 1"))
    def test_or3(self):
        self.assertTrue(Validator.is_valid_data_size("or 1 2"))
    def test_or4(self):
        self.assertTrue(Validator.is_valid_data_size("or 1 2 3"))
    def test_or5(self):
        self.assertFalse(Validator.is_valid_data_size("or 1 2a"))

class ValidatorIsValidAccessRule(unittest.TestCase):
    def test_mandatory(self):
        self.assertTrue(Validator.is_valid_access_rule("mandatory"))
    def test_optional(self):
        self.assertTrue(Validator.is_valid_access_rule("optional"))
    def test_(self):
        self.assertTrue(Validator.is_valid_access_rule("-"))
    def test_none(self):
        self.assertFalse(Validator.is_valid_access_rule("none"))

class ValidatorIsValidAnnouncement(unittest.TestCase):
    def test_mandatory(self):
        self.assertTrue(Validator.is_valid_announcement("mandatory"))
    def test_optional(self):
        self.assertFalse(Validator.is_valid_announcement("optional"))
    def test_(self):
        self.assertTrue(Validator.is_valid_announcement("-"))
    def test_none(self):
        self.assertFalse(Validator.is_valid_announcement("none"))

class ValidatorIsValidText(unittest.TestCase):
    def test_null(self):
        self.assertTrue(Validator.is_valid_text(""))
    def test_enter(self):
        self.assertTrue(Validator.is_valid_text("\n"))
    def test_x000a(self):
        self.assertFalse(Validator.is_valid_text("_x000a_"))

if __name__ == "__main__":
    unittest.main()

