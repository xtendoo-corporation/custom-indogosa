# Copyright 2023 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    weight = fields.Float(
        string='Weight',
        readonly=False,
    )
    volume = fields.Float(
        string='Volume',
        readonly=False,
    )
    pallet_units = fields.Integer(
        string='Pallet Units',
        readonly=False,
    )
    box_units = fields.Integer(
        string='Box Units',
        readonly=False,
    )
    package_units = fields.Integer(
        string='Package Units',
        readonly=False,
    )

