from odoo import models, fields, api



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    total_litros = fields.Float(
        string='Total Litros',
        compute='_compute_transport_base',
        store=True,
        precompute=True,
        digits=(16, 2)
    )

    coste_transporte_linea = fields.Float(
        string='Coste Transporte/Litro',
        compute='_compute_transport_base',
        store=True,
        precompute=True,
        digits=(16, 2)
    )

    total_coste_transporte = fields.Float(
        string='Coste Total Transporte',
        compute='_compute_transport_base',
        store=True,
        precompute=True,
        digits=(16, 2)
    )

    # Campos que no pueden ser precomputados
    margin = fields.Float(
        string='Margen',
        compute='_compute_margin_fields',
        store=True,
        precompute=False,  # Explícitamente false
        digits='Product Price'
    )

    margin_percent = fields.Float(
        string='Margen %',
        compute='_compute_margin_fields',
        store=True,
        precompute=False,  # Explícitamente false
    )

    coste_total = fields.Float(
        string='Coste Total',
        compute='_compute_margin_fields',
        store=True,
        precompute=False,  # Explícitamente false
        digits='Product Price'
    )

    # Método para campos precomputables
    @api.depends('product_id', 'product_uom_qty', 'order_id.coste_transporte')
    def _compute_transport_base(self):
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

    # Método separado para campos no precomputables
    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price',
                 'total_litros', 'coste_transporte_linea')
    def _compute_margin_fields(self):
        for line in self:
            # Cálculo del coste total
            product_cost = line.purchase_price * line.product_uom_qty
            transport_cost = line.total_coste_transporte
            line.coste_total = product_cost + transport_cost

            # Cálculo del margen
            line.margin = line.price_subtotal - line.coste_total

            # Cálculo del porcentaje de margen
            if line.price_subtotal:
                line.margin_percent = (line.margin / line.price_subtotal)
            else:
                line.margin_percent = 0.0
