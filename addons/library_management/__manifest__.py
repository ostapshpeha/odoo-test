# -*- coding: utf-8 -*-
# Odoo module manifest — describes this add-on to the Odoo server.
# Odoo reads this dict to know the module name, its dependencies,
# which data files to load, and whether to show it as a standalone app.
{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'summary': 'Manage library books and rentals',
    'description': (
        'A module to manage a library: track books, authors, '
        'publication dates, availability, and book rentals.'
    ),
    'author': 'Developer',
    'category': 'Library',

    # 'base' provides res.partner and other core models we depend on.
    'depends': ['base'],

    # Data files are loaded in the listed order.
    # Security first, then views, then menus (menus reference actions in views).
    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/rent_views.xml',
        'views/wizard_views.xml',
        'views/menu_views.xml',
    ],

    # installable=True means this module can be installed from the Apps menu.
    'installable': True,

    # application=True makes the module appear as a top-level app in the home menu.
    'application': True,
}
