from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_units_sum = fields.Integer(
        string='Total Unidades',
        compute='_compute_total_units_sum',
        store=True,
        help='Suma de las unidades totales de todas las líneas'
    )

    @api.depends('order_line.total_units', 'order_line.product_uom_qty', 'order_line.product_uom_id.factor')
    def _compute_total_units_sum(self):
        for order in self:
            order.total_units_sum = sum(order.order_line.mapped('total_units'))

    coste_transporte = fields.Monetary(
        string='Coste Transporte',
        currency_field='currency_id',
        help='Coste de transporte aplicado a esta orden',
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_coste_transporte(self):
        if self.partner_id and self.partner_id.coste_transporte:
            self.coste_transporte = self.partner_id.coste_transporte


