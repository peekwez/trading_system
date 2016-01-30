# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from django.conf import settings

# if settings is not configured setup
if not settings.configured:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db.settings')
    django.setup()
