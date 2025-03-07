from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    weight_control_ids = fields.One2many(
        'mrp.production.weight.control',
        'production_id',
        string='Weight Controls'
    )
