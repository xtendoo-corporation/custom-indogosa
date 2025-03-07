# Copyright 2023 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    minimum_weight = fields.Float(
        string='Minimum weight',
        readonly=False,
    )
    maximum_weight = fields.Float(
        string='Maximum weight',
        readonly=False,
    )
