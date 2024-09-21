from odoo import  models , fields


class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital department'

    name = fields.Char(string='Name', required=True)
    is_opened = fields.Boolean(string='Is Opened')
    capacity = fields.Integer(string="Capacity")
    doctor_ids = fields.One2many('hms.doctor', 'department_id', string="Doctors")
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")



