# -*- coding: utf-8 -*-
from core.settings.settings import *

# Production settings

PRODUCTION = False

if PRODUCTION:
    from core.settings.production import *
    assert DEBUG == False
    assert SECRET_KEY != 'DEBUG-SECRET-KEY'

# Override settings using this file
