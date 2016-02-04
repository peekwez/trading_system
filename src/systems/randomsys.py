# -*- coding: utf-8 -*-
from __future__ import absolute_import

from random import random

from systems.commonsys import BaseSystem
from systems.bitops import ibset


class RandomSystem(BaseSystem):

    def __flip(self):
        return random()

    def set_signal(self):
        if self.__flip() <= 0.5:
            pos = 0
        else:
            pos = 1
        self.bits = ibset(self.bits,pos)
