from odoo import models, fields, api

class MrpBomLineInherited(models.Model):
    _inherit = 'mrp.bom.line'

    total_price = fields.Float(
        compute='_compute_total_price',
        store=True,
        string='Total Cost',
        digits=(16, 6)
    )

    @api.depends('product_id', 'product_qty', 'standard_price')
    def _compute_total_price(self):
        for res in self:
            res.total_price = res.standard_price * res.product_qty
