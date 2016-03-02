# -*- coding: utf-8 -*-
from core.settings.settings import *

# Production settings

PRODUCTION = False

if PRODUCTION:
    from core.settings.production import *

# Override settings using this file
