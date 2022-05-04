# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
{
    'name': 'Hr Expense Cancel (Refuse)',
    'version': '12.0.1.0',
    'sequence': 1,
    'description': """
          odoo app will help you to cancel hr expense after post expense
        
        Hr Expense Cancel
        Hr Expense Refuse
        Cancel Hr Expense      
        Refuse Hr Expense
Hr Expense Cancel
Odoo Hr Expense Cancel
HR Expense 
Odoo HR Expense
Cancel HR expense
Odoo cancel HR Expense
Refuse HR expense
Odoo refuse hr expense
Cancel Journal Entry related to HR Expense
Odoo Cancel Journal Entry related to HR Expense
Refuse Journal Entry related to HR Expense 
Odoo Refuse Journal Entry related to HR Expense 
Unlink Journal Entry related to HR Expense 
Odoo Unlink Journal Entry related to HR Expense 
Unlink journal entry 
Odoo unlink journal entry 
Unlink HR Expense
Odoo unlink HR Expense 
Manage HR Expense 
Odoo manage HR expense 
Create HR Expense 
Odoo create HR Expense 
Journal entry 
Odoo journal entry
Journal entry of hr expense 
Odoo journal entry of hr expense 
HR expense refuse 
Odoo HR expense refuse 
Refused HR expense 
Odoo refused HR Expense 
Unlinked Journal Entry of HR Expense
Odoo Unlinked Journal Entry of HR Expense
              
    """,
    'summary': 'odoo app will help you to cancel hr expense after post expense',
    "category": 'Generic Modules/Human Resources',
    'depends': ['hr_expense','account_cancel'],
    'data': [
            'views/hr_expense_sheet_views.xml',
            ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':35.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
