# -*- coding: utf-8 -*-

from odoo import fields, models, api 


class SaleOrder(models.Model):

    _inherit="sale.order"

    text_addenda = fields.Char(string="Orden de compra:")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'text_addenda': self.text_addenda,
            
        })
        return invoice_vals