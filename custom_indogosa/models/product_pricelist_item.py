# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"


    global_discount_ids = fields.Many2many(
        comoodel_name="global.discount",
        string="Global Discounts",
        required=False,
        readonly=False,
    )
    global_discount = fields.Float(
        string="Global Discount",
        required=False,
        readonly=False,
    )

    @api.onchange('global_discount_ids')
    def _onchange_global_discount_ids(self):
        if self.global_discount_ids:
            self.global_discount = sum(self.global_discount_ids.mapped('discount')) / len(self.global_discount_ids)
        else:
            self.global_discount = 0.0

