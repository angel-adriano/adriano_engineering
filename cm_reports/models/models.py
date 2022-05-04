# -*- coding: utf-8 -*-

# from datetime import timedelta

from odoo import models, fields, api


class CmReports(models.Model):
    _inherit = 'sale.order'

    journal_id = fields.Many2one('account.journal', string='Procesador de pagos:', domain=[('type', 'in', ('bank', 'cash'))])
    delivery_date = fields.Date('Fecha compromiso de envio')

