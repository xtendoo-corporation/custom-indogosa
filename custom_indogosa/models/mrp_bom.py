from odoo import models, fields, api
from odoo.tools import float_round

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    total_bom_price = fields.Float(
        string='Precio Total Coste',
        compute='_compute_total_bom_price',
        store=True,
        digits=(16, 6)
    )

    @api.depends('bom_line_ids.total_price')
    def _compute_total_bom_price(self):
        for bom in self:
            total = sum(line.total_price for line in bom.bom_line_ids)
            bom.total_bom_price = float_round(total, precision_digits=6)
