# -*- coding: utf-8 -*-
from __future__ import absolute_import

from systems.bitops import btest, ibclr


signals = ((0,'buy'),(1,'sell'),)
def trigger(func):
  def wrapper(self, *args, **kwargs):

    # set signal bit and reset signal value
    self.set_signal()
    self.signal = ''

    # trigger signal based on bit value
    for key,value in signals:
      if btest(self.bits,key):
        self.bits  = ibclr(self.bits,key)
        self.signal = value
        return func(self)
  return wrapper

class BaseSystem(object):

  def __init__(self):
    self.bits = 0b100
    self.len_bits = self.bits.bit_length()-1
    self.signal = ''

  @trigger
  def get_signal(self):
    return self.signal

  def set_signal(self):
    """Define logic for setting a signal here"""
    pass
