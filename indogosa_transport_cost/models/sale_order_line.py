from odoo import models, fields, api



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    total_units = fields.Integer(
        string='Unidades totales',
        compute='_compute_total_units'
    )

    @api.depends('product_uom_qty', 'product_uom')
    def _compute_total_units(self):
        for line in self:
            line.total_units = line.product_uom_qty * line.product_uom.ratio

    # precompute=False (bug real encontrado migrando a 18.0, no estaba antes):
    # este campo depende de order_id.total_units_sum, un campo computado del
    # PEDIDO que a su vez depende de las lineas hermanas. Con precompute=True,
    # al crear pedido+lineas en una sola llamada create() (el flujo normal al
    # guardar un pedido nuevo desde el formulario), Odoo calcula este campo
    # ANTES de que total_units_sum del pedido este resuelto, y el resultado
    # queda fijado en 0 sin volver a recalcularse nunca (verificado en vivo:
    # con precompute=True el campo queda en 0.0 tras un create() atomico
    # aunque total_units_sum del pedido SI se calcula bien). Mismo motivo por
    # el que margin/margin_percent/coste_total ya llevaban precompute=False
    # mas abajo — aqui faltaba aplicar el mismo criterio.
    coste_transporte_linea = fields.Float(
        string='Coste Transporte',
        compute='_compute_transport_base',
        store=True,
        precompute=False,
        digits=(16, 6)
    )

    total_coste_transporte = fields.Float(
        string='Coste Total Transporte',
        compute='_compute_transport_base',
        store=True,
        precompute=False,
        digits=(16, 6)
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
    @api.depends('product_id','total_units', 'order_id.total_units_sum', 'order_id.coste_transporte')
    def _compute_transport_base(self):
        for line in self:
            if line.order_id.coste_transporte and line.order_id.total_units_sum > 0:
                coste_unitario = line.order_id.coste_transporte / line.order_id.total_units_sum
                line.coste_transporte_linea = coste_unitario
                line.total_coste_transporte = coste_unitario * line.total_units
            else:
                line.coste_transporte_linea = 0.0
                line.total_coste_transporte = 0.0

    # Método separado para campos no precomputables
    @api.depends('price_subtotal', 'purchase_price', 'total_units', 'total_coste_transporte')
    def _compute_margin_fields(self):
        for line in self:
            line.coste_total = line.total_coste_transporte + line.purchase_price
            line.margin = line.price_subtotal - line.coste_total
            if line.price_subtotal:
                line.margin_percent = (line.margin / line.price_subtotal)
            else:
                line.margin_percent = 0.0
