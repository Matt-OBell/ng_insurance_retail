# -*- coding: utf-8 -*-
{
    'name': "Retailing Insurance Management",

    'summary': """
        Manage the retailing of insurance policies""",

    'description': """
        Manage the retailing of insurance policies
    """,

    'author': "Mattobell",
    'website': "http://www.mattobell.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'retail',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'crm', 'product', 'website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'actions.xml',
        # 'menus.xml',
        'views/views.xml',
        'views/res_partner.xml',
        'templates/forms.xml',
        'templates/subscriber.xml',
        'templates/policies.xml',
        'templates/assets/assets.xml',
        'data/product_product.xml',
        'data/policy_type.xml',
        'data/website_menu.xml',
        'actions.xml',
        'menus.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'application': True,
}