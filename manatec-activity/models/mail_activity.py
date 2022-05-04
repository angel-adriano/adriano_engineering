# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _

#  Author: Tobias Reinwarth (tobias.reinwarth@manatec.de)
#  Copyright: 2019, manaTec GmbH
#  Date created: 4.3.2019


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.one
    @api.depends('res_model', 'res_id')
    def _compute_res_url(self):
        self.res_url = '#id=%s&model=%s' % (self.res_id, self.res_model)

    res_url = fields.Char(string='Related Document Url', help='Link to related document.', compute=_compute_res_url)

