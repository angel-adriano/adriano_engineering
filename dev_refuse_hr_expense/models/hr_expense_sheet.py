# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class hr_expense_sheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    
    @api.multi
    def refuse_sheet(self, reason):
        res = super(hr_expense_sheet,self).refuse_sheet(reason)
        account_move = self.env['account.move']
        for sheet in self:
            account_move_id = sheet.account_move_id
            if account_move_id:
                account_move_id.button_cancel()
                sheet.account_move_id = False
                account_move_id.unlink()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
