# -*- coding: utf-8 -*-
from __future__ import absolute_import


class BitOperationsError(Exception):
  '''
  Raises an exception if bit operation fails
  '''

  def __init__(self,message):
    self.message = message

  def __str__(self):
    return repr(self.message)


class BitOperations:

  '''
  A class for checking, setting and clearing a bit value
  '''

  @staticmethod
  def btest(i,pos):
    '''
    Returns a boolean if the bit at ``pos`` is turned on or off
    '''
    return bool(i & (1 << pos))

  @staticmethod
  def ibset(i,pos):
    '''
    Sets the bit value at ``pos`` to one
    '''
    if btest(i,pos):
      raise BitOperationsError('Bit is already turned on')
    else:
      return i + (1 << pos)

  @staticmethod
  def ibclr(i,pos):
    '''
    Sets the ``bit`` value at pos to zero
    '''
    if not(btest(i,pos)):
      raise BitOperationsError('Bit is already turned off')
    else:
      return i - (1 << pos)

btest = BitOperations.btest
ibset = BitOperations.ibset
ibclr = BitOperations.ibclr
