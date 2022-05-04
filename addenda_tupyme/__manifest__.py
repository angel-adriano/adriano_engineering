# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Addenda Whirlpool',
    'version': '2.2',
    'description': ''' Agrega campos para agregar addenda de texto
    ''',    
    'category': 'Accounting',
    'author': 'FTNMX',
    'website': 'www.ftn.mx',
    'depends': [
        'cdfi_invoice','sale',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/sale_order_view.xml'
        #'views/res_company_view.xml',
        #'views/sale_view.xml',
        #'report/invoice_report.xml',	
	],
    'application': False,
    'installable': True,
}
