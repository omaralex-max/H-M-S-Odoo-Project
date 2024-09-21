from odoo import  models , fields , api


class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctors'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    image = fields.Binary(string='Image')
    patient_ids = fields.Many2many('hms.patient', 'doctor_ids', string="Patient")
    department_id = fields.Many2one('hms.department', string="Department", ondelete='set null')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for doctor in self:
            doctor.name = f"{doctor.first_name} {doctor.last_name}"