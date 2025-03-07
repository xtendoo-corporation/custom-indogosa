from odoo import models, fields, api

class MrpProductionWeightControl(models.Model):
    _name = 'mrp.production.weight.control'
    _description = 'Weight Control for Manufacturing Orders'

    production_id = fields.Many2one(
        comodel_name='mrp.production',
        string='Manufacturing Order',
        required=True,
        ondelete='cascade'
    )
    weight = fields.Float(
        string='Weight',
        required=True,
        digits=(16, 6)
    )
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        required=True
    )
    minimum_weight = fields.Float(
        string='Minimum Weight',
        related='production_id.product_id.minimum_weight',
        readonly=True
    )
    maximum_weight = fields.Float(
        string='Maximum Weight',
        related='production_id.product_id.maximum_weight',
        readonly=True
    )
    is_weight_control = fields.Boolean(
        string='Is Weight OK?',
        compute='_compute_is_weight_control',
        store=True
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=True
    )

    @api.depends('weight', 'minimum_weight', 'maximum_weight')
    def _compute_is_weight_control(self):
        for record in self:
            record.is_weight_control = record.minimum_weight <= record.weight <= record.maximum_weight

