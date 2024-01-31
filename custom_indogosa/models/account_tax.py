# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    amount = fields.Float(
        required=True,
        digits=(16, 6),
        default=0.0,
    )
