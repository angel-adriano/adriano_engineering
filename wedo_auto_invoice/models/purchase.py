# -*- coding: utf-8 -*-
# Copyright 2020 WeDo Technology
# Website: http://wedotech-s.com
# Email: apps@wedotech-s.com
# Phone:00249900034328 - 00249122005009

from odoo import api, models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def create_invoice(self):
        bill = self.env['account.invoice']

        bill = bill.new({
            'date': fields.date.today(),
            'partner_id': self.partner_id.id,
            'ref': self.partner_ref,
            'company_id': self.company_id.id,
            'invoice_payment_term_id': self.payment_term_id.id,
            'currency_id': self.currency_id.id,
            'fiscal_position_id': self.fiscal_position_id,
            'type': 'in_invoice',
            'purchase_id': self.id,
            'origin': self.name,
        })
        bill.purchase_order_change()
        invoice_vals = bill._convert_to_write(bill._cache)
        #self.invoice_ids += bill
        self.env['account.invoice'].create(invoice_vals)

    def _get_invoiced(self):
        super(PurchaseOrder, self)._get_invoiced()
        if self.invoice_status == 'to invoice' and self.company_id.auto_invoice:
            self.create_invoice()
            super(PurchaseOrder, self)._get_invoiced()


