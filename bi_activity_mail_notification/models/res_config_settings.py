# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class res_company(models.Model):
	_inherit = 'res.company'

	activity_email_notification = fields.Boolean(string='Activity Notification')
	edit_notification = fields.Boolean(string='Activity Edit Notification')
	edit_create_user = fields.Boolean(string='Notify Create User')
	edit_assignee_user = fields.Boolean(string='Notify Assignee User')
	done_notification = fields.Boolean(string='Activity Done Notification')
	done_create_user = fields.Boolean(string='Notify Create User')
	done_assignee_user = fields.Boolean(string='Notify Assignee User')
	cancel_notification = fields.Boolean(string='Activity Cancel Notification')
	cancel_create_user = fields.Boolean(string='Notify Create User')
	cancel_assignee_user = fields.Boolean(string='Notify Assignee User')

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'
	
	activity_email_notification = fields.Boolean(string='Activity Notification',related='company_id.activity_email_notification',readonly=False)
	edit_notification = fields.Boolean(string='Activity Edit Notification',related='company_id.edit_notification',readonly=False)
	edit_create_user = fields.Boolean(string='Notify Create User',related='company_id.edit_create_user',readonly=False)
	edit_assignee_user = fields.Boolean(string='Notify Assignee User',related='company_id.edit_assignee_user',readonly=False)
	done_notification = fields.Boolean(string='Activity Done Notification',related='company_id.done_notification',readonly=False)
	done_create_user = fields.Boolean(string='Notify Create User',related='company_id.done_create_user',readonly=False)
	done_assignee_user = fields.Boolean(string='Notify Assignee User',related='company_id.done_assignee_user',readonly=False)
	cancel_notification = fields.Boolean(string='Activity Cancel Notification',related='company_id.cancel_notification',readonly=False)
	cancel_create_user = fields.Boolean(string='Notify Create User',related='company_id.cancel_create_user',readonly=False)
	cancel_assignee_user = fields.Boolean(string='Notify Assignee User',related='company_id.cancel_assignee_user',readonly=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: