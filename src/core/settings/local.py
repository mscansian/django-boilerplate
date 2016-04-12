# -*- coding: utf-8 -*-
import os

from core.settings.settings import *

# Production settings

PRODUCTION = os.path.isfile(os.path.expanduser('~/.django-production'))

if PRODUCTION:
    from core.settings.production import *
    assert DEBUG == False
    assert SECRET_KEY != 'DEBUG-SECRET-KEY'

# Override settings using this file (not recommended if using git as deployment method)
