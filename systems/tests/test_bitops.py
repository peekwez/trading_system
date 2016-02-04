# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

from systems.bitops import btest, ibset, ibclr, BitOperationsError

# UNIT TESTS
class test_bitwise_operations(unittest.TestCase):

  __bit_pos  = range(8)
  __off_bits = __bit_pos[0::2]
  __on_bits  = __bit_pos[1::2]

  @property
  def val(self):
    return 0b10101010 # right to left

  def __set_bit(self,i,pos):
    return ibset(i,pos)

  def __clear_bit(self,i,pos):
    return ibclr(i,pos)

  def test_bit_on(self):
    for pos in self.__on_bits:
      ival = self.val
      self.assertEqual(btest(ival, pos), True)

  def test_bit_off(self):
    for pos in self.__off_bits:
      ival = self.val
      self.assertEqual(btest(ival, pos), False)

  def test_failed_set_bit(self):
    for pos in self.__on_bits:
      ival = self.val
      args = (ival, pos)
      self.assertRaises(BitOperationsError,
                        self.__set_bit, *args)

  def test_failed_clear_bit(self):
    for pos in self.__off_bits:
      ival = self.val
      args = (ival, pos)
      self.assertRaises(BitOperationsError,
                        self.__clear_bit, *args)

  def test_set_bit(self):
    for pos in self.__off_bits:
      ival = self.val
      jval = self.__set_bit(ival, pos)
      self.assertEqual(btest(jval, pos), True)

  def test_clear_bit(self):
    for pos in self.__on_bits:
      ival = self.val
      jval = self.__clear_bit(ival, pos)
      self.assertEqual(btest(jval, pos), False)
