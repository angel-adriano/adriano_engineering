# -*- coding: utf-8 -*-
{
    'name': "AEN Custom Reports",

    'summary': """
        Formatos de factura, orden de compra y cotizaciones de Adriano Engineering""",

    'description': """
        Long description of module's purpose
    """,

    'author': "FTNMX",
    'website': "https://formalizatunegocio.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'purchase', 'sale', 'complemento_leyenda', 'addenda_tupyme',
                ],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/invoice_report.xml',
        'views/sale_report_templates.xml',
        'views/purchase_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
