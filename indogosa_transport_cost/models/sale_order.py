from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coste_transporte = fields.Monetary(
        string='Coste Transporte',
        currency_field='currency_id',
        help='Coste de transporte aplicado a esta orden'
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_coste_transporte(self):
        if self.partner_id and self.partner_id.coste_transporte:
            self.coste_transporte = self.partner_id.coste_transporte


