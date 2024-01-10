# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    global_discount_ids = fields.Many2many(
        comodel_name="global.discount",
        string="Sale Global Discounts",
        domain="[('discount_scope', '=', 'sale'), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
    )
    price_discounted = fields.Float(
        string="Price Discounted",
        required=False,
        readonly=True,
    )
    product_price_discounted = fields.Float(
        string="Product Price Discounted",
        required=False,
        readonly=True,
    )

    @api.onchange('global_discount_ids', 'fixed_price')
    def _onchange_global_discount_ids(self):
        base = self.fixed_price
        if self.global_discount_ids:
            for discount in self.global_discount_ids:
                base = discount._get_global_discount_vals(base)["base_discounted"]
        self.price_discounted = base

    @api.onchange('global_discount_ids', 'product_tmpl_id')
    def _onchange_product_price_id(self):
        base = self.product_tmpl_id.standard_price
        print("BASE", base)
        if self.global_discount_ids:
            for discount in self.global_discount_ids:
                base = discount._get_global_discount_vals(base)["base_discounted"]
        print("BASE 2", base)
        self.product_price_discounted = base
