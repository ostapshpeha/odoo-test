# -*- coding: utf-8 -*-
# Top-level package init for the library_management module.
# Odoo imports this file when the module is loaded; it must import every
# sub-package that contains Python code Odoo needs to register
# (models, controllers, wizards, etc.).

# Import ORM models and transient models (wizards).
from . import models

# Import HTTP controllers so Odoo registers the /library/books route.
from . import controllers
