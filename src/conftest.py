# --*-- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import pytest

@pytest.fixture(scope='module')
def dbase(request, _django_db_setup, _django_cursor_wrapper):
    from pytest_django.fixtures import _django_db_fixture_helper
    return _django_db_fixture_helper(False, request, _django_cursor_wrapper)
