# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import django

# setup django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db.db.settings')
django.setup()
