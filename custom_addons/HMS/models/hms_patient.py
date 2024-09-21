from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    birth_date = fields.Date(string="Birth Date")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection([
        ('1', 'A'),
        ('2', 'B'),
        ('3', 'AB'),
        ('4', 'O'),
        ('5', 'A+'),
        ('6', 'B+'),
        ('7', 'A-'),
        ('8', 'B-'),
    ], string="Blood Type")
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string="Age", compute='_compute_age')
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors' , domain="[('department_id', '=', department_id)]")
    department_id = fields.Many2one('hms.department', string="Department", ondelete='set null' , domain="[('is_opened', '=', True)]")
    history_line_ids = fields.One2many('hms.patient.history', 'patient_id')
    department_capacity = fields.Integer(string="Department Capacity", compute='_compute_department_capacity', store=True)
    state = fields.Selection([
        ('consultation', 'Consultation'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged')
    ], string="State", default='consultation', required=True, tracking=True)


    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for patient in self:
            patient.name = f"{patient.first_name} {patient.last_name}"

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = 0

    @api.depends('department_id')
    def _compute_department_capacity(self):
        for rec in self:
            if rec.department_id:
                rec.department_capacity = rec.department_id.capacity
            else:
                rec.department_capacity = 0
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                "warning": {
                    'title': "PCR Field Checked",
                    'message': "PCR field has been checked automatically"
                }
            }

    @api.depends('age')
    def _compute_history_visible(self):
        for rec in self:
            rec.history_visible = rec.age >= 50

    @api.constrains('cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError('CR Ratio is required when PCR is checked.')

    def action_set_consultation(self):
        self._change_state('consultation')

    def action_admit_patient(self):
        self._change_state('admitted')

    def action_discharge_patient(self):
        self._change_state('discharged')

    def _change_state(self, new_state):
        for rec in self:
            old_state = rec.state
            rec.state = new_state
            self.env['hms.patient.history'].create({
                'patient_id': rec.id,
                'name': f'State changed to {new_state}',
                'date': fields.Date.today(),
                'history_line': f'State changed from {old_state} to {new_state}'
            })

    @api.constrains('doctor_ids')
    def _check_doctor_and_department(self):
        for rec in self:
            if rec.doctor_ids and not rec.department_id:
                raise ValidationError('Please select a department before assigning a doctor.')


class PatientHistory(models.Model):
    _name = 'hms.patient.history'
    _description = 'Patient History'

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    history_line = fields.Html(string="History Line", required=True)
    patient_id = fields.Many2one('hms.patient', string="Patient", required=True)
