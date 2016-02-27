# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest
from systems.bitops import btest, ibset, ibclr, BitOperationsError

pytestmark = pytest.mark.django_db

class TestBitOperations:

  val = 0b10101010 # right to left
  __bit_pos  = range(8)
  __off_bits = __bit_pos[0::2]
  __on_bits  = __bit_pos[1::2]

  def test_bit_on(self):
    for pos in self.__on_bits:
      ival = self.val
      assert btest(ival, pos) == True

  def test_bit_off(self):
    for pos in self.__off_bits:
      ival = self.val
      assert btest(ival, pos) == False

  def test_failed_set_bit(self):
    for pos in self.__on_bits:
      ival = self.val
      args = (ival, pos)
      with pytest.raises(BitOperationsError):
        ibset(*args)

  def test_failed_clear_bit(self):
    for pos in self.__off_bits:
      ival = self.val
      args = (ival, pos)
      with pytest.raises(BitOperationsError):
        ibclr(*args)

  def test_set_bit(self):
    for pos in self.__off_bits:
      ival = self.val
      jval = ibset(ival, pos)
      assert btest(jval, pos) == True

  def test_clear_bit(self):
    for pos in self.__on_bits:
      ival = self.val
      jval = ibclr(ival, pos)
      assert btest(jval, pos) == False
