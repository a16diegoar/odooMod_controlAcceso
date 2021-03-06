# -*- coding: utf-8 -*-
{
    'name': "control_acceso",

    'summary': """
        Control de acceso""",

    'description': """
        Módulo con mecanismos que permiten registrar y controlar el uso de salas por parte del personal
    """,

    'author': "Diego Antelo Rútolo",
    'website': "http://rutolo.eu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/user_actions.xml',
        'views/acceso.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}