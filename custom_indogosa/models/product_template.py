# Copyright 2023 Manuel Calero - Xtendoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ufi = fields.Char(
        string='Ufi',
        readonly=False,
    )
    dun14 = fields.Char(
        string='Dun 14',
        readonly=False,
    )
    long = fields.Float(
        string='Long',
        readonly=False,
    )
    high = fields.Float(
        string='High',
        readonly=False,
    )
    broad = fields.Float(
        string='Broad',
        readonly=False,
    )
    weight_box = fields.Float(
        string='Box weight',
        readonly=False,
    )
    volume_box = fields.Float(
        string='Box volume',
        readonly=False,
    )
    long_box = fields.Float(
        string='Box long',
        readonly=False,
    )
    high_box = fields.Float(
        string='Box high',
        readonly=False,
    )
    broad_box = fields.Float(
        string='Box broad',
        readonly=False,
    )
    box_pallet = fields.Integer(
        string='Number of box',
        readonly=False,
    )
    base_pallet = fields.Integer(
        string='Box broad',
        readonly=False,
    )
    height_pallet = fields.Integer(
        string='Box broad',
        readonly=False,
    )
