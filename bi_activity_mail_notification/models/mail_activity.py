# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    assign_id = fields.Many2one(
        'res.users', 'Assigned',
        default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Partner')
    mail_url = fields.Char(string="url", compute="_compute_url")
    activity_status = fields.Char(string="status")
    activity_feedback_email = fields.Char(string="feedback")

    def _compute_url(self):
        for activity in self:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            static_url = "/web"
            view_id = "?db=%s#id=%s" % (self._cr.dbname, activity.res_id)
            view_type = "&view_type=form&model=%s" % (activity.res_model)
            mail_url_id = str(base_url) + static_url + view_id + view_type
            activity.update({
                'mail_url' : mail_url_id
            })

    @api.model
    def create(self, values):
        activity = super(MailActivity, self).create(values)
        activity.write({'activity_status':'create'})
        return activity

    def action_create_calendar_event(self):
        self.action_close_dialog()
        activity = super(MailActivity, self).action_create_calendar_event()
        return activity

    def action_close_dialog(self):
        if self.activity_status != 'create':
            res_config_settings_obj = self.env['res.config.settings'].search([],limit=1,order="id desc")
            context = self._context
            current_uid = context.get('uid')
            user_id = self.env['res.users'].sudo().browse(current_uid)
            email_to = []
            email_to_assignee = []
            if user_id:
                if self.env.user.company_id.activity_email_notification == True:
                    if self.env.user.company_id.edit_notification == True:
                        if self.env.user.company_id.edit_create_user == True:
                            for user in self.create_user_id:
                                email_to.append(user.partner_id.id)
                            template_id = self.env['ir.model.data'].get_object_reference('bi_activity_mail_notification', 'email_template_edit_notification')[1]
                            email_template_obj = self.env['mail.template'].browse(template_id)
                            if self.summary:
                                body_html = '''
                                <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
                                    <p>Dear <b>{0},</b></p><br/>
                                    <p>Your Scheduled Activity | {1} - {2} of document  {3} has been modified by {4}. </p><br/>
                                    <h4>Details:-</h4>
                                    <b>Summary: </b>{5}<br/></br>
                                    <b>Due date: </b>{7}<br/></br>
                                    <b>Description: </b>{6}
                                </div>
                                <br/>
                                <div style="margin: 16px 0px 16px 0px; font-size: 14px;">
                                    <a href='{8}'
                                    style="background-color:#875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
                                    View <t t-esc="model_description or 'document'"/>
                                    </a>
                                </div>
                                '''.format(
                                    self.create_user_id.name, self.activity_type_id.name, self.summary,self.res_name,self.assign_id.name,self.summary,self.note,self.date_deadline,self.mail_url)
                            else:
                                body_html = '''
                                <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
                                    <p>Dear <b>{0},</b></p><br/>
                                    <p>Your Scheduled Activity | {1} of document  {2} has been modified by {3}. </p><br/>
                                    <h4>Details:-</h4>
                                    <b>Summary: </b>{4}<br/></br>
                                    <b>Due date: </b>{6}<br/></br>
                                    <b>Description: </b>{5}
                                </div>
                                <br/>
                                <div style="margin: 16px 0px 16px 0px; font-size: 14px;">
                                    <a href='{7}'
                                    style="background-color:#875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
                                    View <t t-esc="model_description or 'document'"/>
                                    </a>
                                </div>
                                '''.format(
                                    self.create_user_id.name, self.activity_type_id.name,self.res_name,self.assign_id.name,'',self.note,self.date_deadline,self.mail_url)
                            if template_id:
                                if self.id:
                                    values = email_template_obj.generate_email(self.id, fields=None)
                                    values['email_from'] = user_id.partner_id.email
                                    values['recipient_ids'] = [(4, pid) for pid in email_to]
                                    values['author_id'] = user_id.partner_id.id
                                    values['res_id'] = False
                                    values['model'] = False
                                    values['body_html'] = body_html
                                    mail_mail_obj = self.env['mail.mail']
                                    msg_id = mail_mail_obj.create(values)
                                    if msg_id:
                                        mail_mail_obj.send([msg_id])
                                        msg_id.sudo().send()
                        if self.env.user.company_id.edit_assignee_user == True:
                            for user in self.user_id:
                                email_to_assignee.append(user.partner_id.id)
                            if self.user_id.id != self.create_user_id.id or self.env.user.company_id.cancel_create_user == False:
                                template_id = self.env['ir.model.data'].get_object_reference('bi_activity_mail_notification', 'email_template_edit_notification_assignee')[1]
                                email_template_obj = self.env['mail.template'].browse(template_id)
                                if self.summary:
                                    body_html = '''
                                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
                                        <p>Dear <b>{0},</b></p><br/>
                                        <p>Your Scheduled Activity | {1} - {2} of document  {3} has been modified by {4}. </p><br/>
                                        <h4>Details:-</h4>
                                        <b>Summary: </b>{5}<br/></br>
                                        <b>Due date: </b>{7}<br/></br>
                                        <b>Description: </b>{6}
                                    </div>
                                    <br/>
                                    <div style="margin: 16px 0px 16px 0px; font-size: 14px;">
                                        <a href='{8}'
                                        style="background-color:#875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
                                        View <t t-esc="model_description or 'document'"/>
                                        </a>
                                    </div>
                                    '''.format(
                                        self.user_id.name, self.activity_type_id.name, self.summary,self.res_name,self.assign_id.name,self.summary,self.note,self.date_deadline,self.mail_url)
                                else:
                                    body_html = '''
                                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">
                                        <p>Dear <b>{0},</b></p><br/>
                                        <p>Your Scheduled Activity | {1} of document  {2} has been modified by {3}. </p><br/>
                                        <h4>Details:-</h4>
                                        <b>Summary: </b>{4}<br/></br>
                                        <b>Due date: </b>{6}<br/></br>
                                        <b>Description: </b>{5}
                                    </div>
                                    <br/>
                                    <div style="margin: 16px 0px 16px 0px; font-size: 14px;">
                                        <a href='{7}'
                                        style="background-color:#875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
                                        View <t t-esc="model_description or 'document'"/>
                                        </a>
                                    </div>
                                    '''.format(
                                        self.user_id.name, self.activity_type_id.name,self.res_name,self.assign_id.name,'',self.note,self.date_deadline,self.mail_url)
                            
                                if template_id:
                                    if self.id:
                                        values = email_template_obj.generate_email(self.id, fields=None)
                                        values['email_from'] = user_id.partner_id.email
                                        values['recipient_ids'] = [(4, pid) for pid in email_to_assignee]
                                        values['author_id'] = user_id.partner_id.id
                                        values['res_id'] = False
                                        values['model'] = False
                                        values['body_html'] = body_html
                                        mail_mail_obj = self.env['mail.mail']
                                        msg_id = mail_mail_obj.create(values)
                                        if msg_id:
                                            mail_mail_obj.send([msg_id])
                                            msg_id.sudo().send()
        self.write({'activity_status':'write'})
        return {'type': 'ir.actions.act_window_close'}

    def action_feedback(self, feedback=False):
        self.write({'activity_feedback_email':feedback})
        res_config_settings_obj = self.env['res.config.settings'].search([],limit=1,order="id desc")
        context = self._context
        current_uid = context.get('uid')
        user_id = self.env['res.users'].sudo().browse(current_uid)
        email_to = []
        email_to_assignee = []
        if user_id:
            if self.env.user.company_id.activity_email_notification == True:
                if self.env.user.company_id.done_notification == True:
                    if self.env.user.company_id.done_create_user == True:
                        for user in self.create_user_id:
                            email_to.append(user.partner_id.id)
                        template_id = self.env['ir.model.data'].get_object_reference('bi_activity_mail_notification', 'email_template_done_notification')[1]
                        email_template_obj = self.env['mail.template'].browse(template_id)
                        if template_id:
                            if self.id:
                                values = email_template_obj.generate_email(self.id, fields=None)
                                values['email_from'] = user_id.partner_id.email
                                values['recipient_ids'] = [(4, pid) for pid in email_to]
                                values['author_id'] = user_id.partner_id.id
                                values['res_id'] = False
                                values['model'] = False
                                mail_mail_obj = self.env['mail.mail']
                                msg_id = mail_mail_obj.create(values)
                                if msg_id:
                                    mail_mail_obj.send([msg_id])
                                    msg_id.sudo().send()
                    if self.env.user.company_id.done_assignee_user == True:
                        for user in self.user_id:
                            email_to_assignee.append(user.partner_id.id)
                        if self.user_id.id != self.create_user_id.id or self.env.user.company_id.cancel_create_user == False:
                            template_id = self.env['ir.model.data'].get_object_reference('bi_activity_mail_notification', 'email_template_done_notification_assignee')[1]
                            email_template_obj = self.env['mail.template'].browse(template_id)
                            if template_id:
                                if self.id:
                                    values = email_template_obj.generate_email(self.id, fields=None)
                                    values['email_from'] = user_id.partner_id.email
                                    values['recipient_ids'] = [(4, pid) for pid in email_to_assignee]
                                    values['author_id'] = user_id.partner_id.id
                                    values['res_id'] = False
                                    values['model'] = False
                                    mail_mail_obj = self.env['mail.mail']
                                    msg_id = mail_mail_obj.create(values)
                                    if msg_id:
                                        mail_mail_obj.send([msg_id])
                                        msg_id.sudo().send()
        self.update({'activity_status':'done',})
        res = super(MailActivity, self).action_feedback()
        
        return res

    def unlink(self):
        if self.activity_status != 'done' or self.activity_status == 'write':
            res_config_settings_obj = self.env['res.config.settings'].search([],limit=1,order="id desc")
            current_uid = self._uid
            user_id = self.env['res.users'].sudo().browse(current_uid)
            email_to = []
            email_to_assignee = []
            if user_id:
                if self.env.user.company_id.activity_email_notification == True:
                    if self.env.user.company_id.cancel_notification == True:
                        if self.env.user.company_id.cancel_create_user == True:
                            for user in self.create_user_id:
                                email_to.append(user.partner_id.id)
                            template_id = self.env['ir.model.data'].get_object_reference('bi_activity_mail_notification', 'email_template_cancel_notification')[1]
                            email_template_obj = self.env['mail.template'].browse(template_id)
                            if template_id:
                                if self.id:
                                    values = email_template_obj.generate_email(self.id, fields=None)
                                    values['email_from'] = user_id.partner_id.email
                                    values['recipient_ids'] = [(4, pid) for pid in email_to]
                                    values['author_id'] = user_id.partner_id.id
                                    values['res_id'] = False
                                    values['model'] = False
                                    mail_mail_obj = self.env['mail.mail']
                                    msg_id = mail_mail_obj.create(values)
                                    if msg_id:
                                        mail_mail_obj.send([msg_id])
                                        msg_id.sudo().send()
                        if self.env.user.company_id.cancel_assignee_user == True:
                            for user in self.user_id:
                                email_to_assignee.append(user.partner_id.id)
                            if self.user_id.id != self.create_user_id.id or self.env.user.company_id.cancel_create_user == False:
                                template_id = self.env['ir.model.data'].get_object_reference('bi_activity_mail_notification', 'email_template_cancel_notification_assignee')[1]
                                email_template_obj = self.env['mail.template'].browse(template_id)
                                if template_id:
                                    if self.id:
                                        values = email_template_obj.generate_email(self.id, fields=None)
                                        values['email_from'] = user_id.partner_id.email
                                        values['recipient_ids'] = [(4, pid) for pid in email_to_assignee]
                                        values['author_id'] = user_id.partner_id.id
                                        values['res_id'] = False
                                        values['model'] = False
                                        mail_mail_obj = self.env['mail.mail']
                                        msg_id = mail_mail_obj.create(values)
                                        if msg_id:
                                            mail_mail_obj.send([msg_id])
                                            msg_id.sudo().send()
        return super(MailActivity, self).unlink()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: