from odoo import models, fields


class Todo(models.Model):
    _name = "test.todo"
    _description = 'Abstract Recurring Contract Line'

    name = fields.Char("Name")
    status = fields.Selection(selection=[("draft", "Draft"), ("done", "Done")])
