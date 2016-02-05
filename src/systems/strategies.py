# -*- coding: utf-8 -*-
from __future__ import absolute_import

from random import random, randint

# import bit operation functions
from systems.bitops import btest, ibclr, ibset


signals = (
    ('short',(1,-1), 0b110),
    ('long', (-1,1), 0b101),
)


# signal trigger decorator
def trigger(func):
    def wrapper(self, *args, **kwargs):

        # set signal bit and reset signal value
        self.set_signal()
        self.signal = ('',(0,0))

        # trigger signal based on bit value
        for name, signal, bits in signals:
            if bits == self.bits:
                self.signal = (name,signal)
                self.reset_bits()
                break
        return func(self)
    return wrapper


class BaseStrategy(object):
    """
    Base class for defining a trading system
    """

    def __init__(self):
        self.bits = 0b100
        self.len_bits = self.bits.bit_length()-1
        self.signal = ('',(0,0))

    def reset_bits(self):
        self.bits = 0b100

    @trigger
    def get_signal(self):
        return self.signal

    def set_signal(self):
        """Define logic for setting a signal here"""
        pass


class RandomStrategy(BaseStrategy):
    """
    A random entry and exit trading system
    """

    def __init__(self,flip=True,*args,**kwargs):
        self.flip = flip
        super(RandomStrategy,self).__init__(*args,**kwargs)

    def set_signal(self):
        if self.flip:
            self.__flip_signal()
        else:
            self.__random_signal()

    def __flip(self):
        return random()

    def __random(self):
        return randint(0,9)

    def __flip_signal(self):
        if self.__flip() <= 0.5: # long position
             self.bits = ibset(self.bits,0)
        else: # short position
            self.bits = ibset(self.bits,1)

    def __random_signal(self):
        if self.__random() == 0: # long position
            self.bits = ibset(self.bits,0)
        elif self.__random() == 1: # short position
            self.bits = ibset(self.bits,1)
