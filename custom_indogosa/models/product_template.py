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
    bottle_box = fields.Float(
        string='Bottle box',
        readonly=False,
    )
    box_pallet = fields.Integer(
        string='Number of box',
        readonly=False,
    )
    base_pallet = fields.Float(
        string='Base pallet',
        readonly=False,
    )
    height_pallet = fields.Float(
        string='Height pallet',
        readonly=False,
    )
    weight_pallet = fields.Float(
        string='Weight pallet',
        readonly=False,
    )
    volume_pallet = fields.Float(
        string='Volume pallet',
        readonly=False,
    )
    layers_pallet = fields.Float(
        string='layers pallet',
        readonly=False,
    )

    @api.model
    def _get_volume_uom_id_from_ir_config_parameter(self):
        """ Get the unit of measure to interpret the `volume` field. By default, we consider
        that volumes are expressed in cubic meters. Users can configure to express them in cubic feet
        or liters by adding an ir.config_parameter record with "product.volume_in_cubic_feet" as key
        and the corresponding value:
        - "1" for cubic feet
        - "2" for liters
        """
        product_volume_param = self.env['ir.config_parameter'].sudo().get_param('product.volume_in_cubic_feet')

        if product_volume_param == '1':
            # Cubic Feet
            return self.env.ref('uom.product_uom_cubic_foot')
        elif product_volume_param == '2':
            # Liters
            return self.env.ref('uom.product_uom_litre')
        else:
            # Default: Cubic Meters
            return self.env.ref('uom.product_uom_cubic_meter')
