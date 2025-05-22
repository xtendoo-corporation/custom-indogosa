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



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    total_litros = fields.Float(
        string='Total Litros',
        compute='_compute_transport_fields',
        compute_sudo=True,
        store=True,
        digits=(16, 2)
    )

    coste_transporte_linea = fields.Float(
        string='Coste Transporte/Litro',
        compute='_compute_transport_fields',
        compute_sudo=True,
        store=True,
        digits=(16, 2)
    )

    total_coste_transporte = fields.Float(
        string='Coste Total Transporte',
        compute='_compute_transport_fields',
        compute_sudo=True,
        store=True,
        digits=(16, 2)
    )

    # Reemplazamos los campos de margen
    margin = fields.Float(
        string='Margen',
        compute='_compute_margin_fields',
        compute_sudo=True,
        store=True,
        digits='Product Price'
    )

    margin_percent = fields.Float(
        string='Margen %',
        compute='_compute_margin_fields',
        compute_sudo=True,
        store=True,
        digits='Product Price'
    )

    # Calculamos todos los campos de transporte en un solo método
    @api.depends('product_id', 'product_uom_qty', 'order_id.coste_transporte')
    def _compute_transport_fields(self):
        for line in self:
            # Cálculo del total de litros
            if line.product_id and line.product_id.volume:
                line.total_litros = line.product_id.volume * line.product_uom_qty
            else:
                line.total_litros = 0.0

            # Cálculo del coste de transporte por litro
            if line.total_litros > 0 and line.order_id.coste_transporte:
                line.coste_transporte_linea = line.order_id.coste_transporte / line.total_litros
            else:
                line.coste_transporte_linea = 0.0

            # Cálculo del coste total de transporte
            line.total_coste_transporte = line.coste_transporte_linea * line.total_litros

    # Cálculo de márgenes en un método separado
    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price',
                 'product_id', 'order_id.coste_transporte')
    def _compute_margin_fields(self):
        for line in self:
            # Calculamos litros y coste de transporte aquí de nuevo para evitar dependencias entre campos computados
            total_litros = 0.0
            if line.product_id and line.product_id.volume:
                total_litros = line.product_id.volume * line.product_uom_qty

            transport_cost = 0.0
            if total_litros > 0 and line.order_id.coste_transporte:
                transport_cost = line.order_id.coste_transporte / total_litros * total_litros

            # Cálculo del coste y margen
            product_cost = line.purchase_price * line.product_uom_qty
            total_cost = product_cost + transport_cost
            line.margin = line.price_subtotal - total_cost

            if line.price_subtotal:
                line.margin_percent = (line.margin / line.price_subtotal) * 100
            else:
                line.margin_percent = 0.0
