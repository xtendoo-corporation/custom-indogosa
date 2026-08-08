# Copyright 2026 Xtendoo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIndogosaTransportCost(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create(
            {"name": "Test partner transport", "coste_transporte": 100.0}
        )
        self.product_a = self.env["product.product"].create(
            {"name": "Product A", "standard_price": 10.0, "list_price": 50.0}
        )
        self.product_b = self.env["product.product"].create(
            {"name": "Product B", "standard_price": 5.0, "list_price": 20.0}
        )
        self.order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "coste_transporte": 100.0,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_a.id,
                            "product_uom_qty": 3.0,
                            "price_unit": 50.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_b.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 20.0,
                        },
                    ),
                ],
            }
        )
        self.line_a = self.order.order_line.filtered(
            lambda l: l.product_id == self.product_a
        )
        self.line_b = self.order.order_line.filtered(
            lambda l: l.product_id == self.product_b
        )

    def test_total_units_per_line(self):
        self.assertEqual(self.line_a.total_units, 3)
        self.assertEqual(self.line_b.total_units, 1)

    def test_total_units_sum_on_order(self):
        self.assertEqual(self.order.total_units_sum, 4)

    def test_transport_cost_distributed_by_units(self):
        # coste_transporte=100 / total_units_sum=4 -> 25 por unidad
        self.assertEqual(self.line_a.coste_transporte_linea, 25.0)
        self.assertEqual(self.line_a.total_coste_transporte, 75.0)
        self.assertEqual(self.line_b.coste_transporte_linea, 25.0)
        self.assertEqual(self.line_b.total_coste_transporte, 25.0)

    def test_transport_cost_zero_without_units(self):
        empty_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        line = self.env["sale.order.line"].create(
            {
                "order_id": empty_order.id,
                "product_id": self.product_a.id,
                "product_uom_qty": 0.0,
                "price_unit": 50.0,
            }
        )
        self.assertEqual(line.coste_transporte_linea, 0.0)
        self.assertEqual(line.total_coste_transporte, 0.0)

    def test_margin_fields(self):
        # coste_total = total_coste_transporte + purchase_price
        # purchase_price viene de sale_margin (standard_price del producto)
        self.assertEqual(self.line_a.coste_total, 75.0 + 10.0)
        self.assertEqual(self.line_a.margin, self.line_a.price_subtotal - 85.0)

    def test_margin_percent_zero_without_subtotal(self):
        empty_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        line = self.env["sale.order.line"].create(
            {
                "order_id": empty_order.id,
                "product_id": self.product_a.id,
                "product_uom_qty": 1.0,
                "price_unit": 0.0,
            }
        )
        self.assertEqual(line.margin_percent, 0.0)

    def test_onchange_partner_sets_transport_cost(self):
        new_order = self.env["sale.order"].new({})
        new_order.partner_id = self.partner
        new_order._onchange_partner_id_coste_transporte()
        self.assertEqual(new_order.coste_transporte, 100.0)

    def test_onchange_partner_without_transport_cost(self):
        other_partner = self.env["res.partner"].create({"name": "No transport cost"})
        new_order = self.env["sale.order"].new({})
        new_order.partner_id = other_partner
        new_order._onchange_partner_id_coste_transporte()
        self.assertEqual(new_order.coste_transporte, 0.0)
