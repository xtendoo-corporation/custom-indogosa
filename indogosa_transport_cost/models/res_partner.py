from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    coste_transporte = fields.Monetary(
        string='Coste Transporte',
        currency_field='currency_id',
        help='Coste de transporte para calcular en órdenes de venta'
    )
