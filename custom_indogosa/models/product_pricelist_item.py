# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    global_discount_ids = fields.Many2many(
        comodel_name="global.discount",
        string="Sale Global Discounts",
        domain="[('discount_scope', '=', 'sale')]",
    )
    price_discounted = fields.Float(
        string="Price Discounted",
        digits=(12, 6),
        store=True,
        required=False,
        readonly=True,
    )
    fixed_price = fields.Float(
        digits=(12, 6),
    )
    product_tmpl_price_cost = fields.Float(
        related="product_tmpl_id.standard_price",
        string="Product Template Price Cost",
        digits=(12, 6),
    )
    product_price_cost = fields.Float(
        related="product_id.standard_price",
        string="Product Price Cost",
        digits=(12, 6),
    )
    product_tmpl_profit_margin = fields.Float(
        string="Product Template Profit Margin",
        store=True,
        digits=(12, 6),
    )
    product_profit_margin = fields.Float(
        string="Product Profit Margin",
        store=True,
        digits=(12, 6),
    )
    product_tmpl_profit_percentage = fields.Float(
        string="Profit Margin (%)",
        store=True,
    )
    product_profit_percentage = fields.Float(
        string="Profit Margin (%)",
        store=True,
    )

    @api.onchange('global_discount_ids', 'fixed_price')
    def _onchange_global_discount_ids(self):
        base = self.fixed_price
        if self.global_discount_ids:
            for discount in self.global_discount_ids:
                base = discount._get_global_discount_vals(base)["base_discounted"]
        self.price_discounted = base

    @api.onchange('product_tmpl_price_cost', 'price_discounted')
    def _onchange_product_tmpl_price_cost(self):
        if self.product_tmpl_price_cost:
            self.product_tmpl_profit_margin = self.price_discounted - self.product_tmpl_price_cost
            self.product_tmpl_profit_percentage = self.product_tmpl_profit_margin / self.product_tmpl_price_cost * 100

    @api.onchange('product_price_cost', 'price_discounted')
    def _onchange_product_price_cost(self):
        if self.product_price_cost:
            self.product_profit_margin = self.price_discounted - self.product_price_cost
            self.product_profit_percentage = self.product_profit_margin / self.product_price_cost * 100
