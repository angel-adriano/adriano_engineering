# -*- coding: utf-8 -*-

# from datetime import timedelta

from odoo import models, fields, api


class CmReports(models.Model):
    _inherit = 'sale.order'

    journal_id = fields.Many2one('account.journal', string='Procesador de pagos:', domain=[('type', 'in', ('bank', 'cash'))])
    delivery_date = fields.Date('Fecha compromiso de envio')
    shopify_sale = fields.Char(string='Orden Shopify', compute='get_shopify_number')
    shop_order_id = fields.Integer(string='ID Shopify', compute='get_shopify_id')

    def get_shopify_id(self):
        for line in self:
            obj = self.env['channel.order.mappings'].search(
                [("odoo_order_id", "=", line.id)], limit=1
            )
            line.shop_order_id = obj.store_order_id

    def get_shopify_number(self):
        for line in self:
            if line.shop_order_id:
                obj = self.env['order.feed'].search(
                [("store_id", "=", line.shop_order_id)], limit=1
            )
                line.shopify_sale = obj.name

