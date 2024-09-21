from odoo import  models , fields


class TodoTicket(models.Model):
    _name = 'todo.ticket'
    _description = 'To-Do Ticket'

    name = fields.Char(string='Ticket Name', required=True)
    number = fields.Integer(string='Ticket Number', required=True)
    tag = fields.Char(string='Tag')
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done')
    ], string='State', default='new')
    file = fields.Binary(string='Attachment')
    description = fields.Text(string='Description')

    def action_new(self):
        self.state = "new"

    def action_doing(self):
        self.state = "doing"

    def action_done(self):
        self.state = "done"