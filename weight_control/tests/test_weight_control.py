# Copyright 2026 Xtendoo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestWeightControl(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env["product.product"].create(
            {
                "name": "Test product weight_control",
                "is_storable": True,
                "minimum_weight": 10.0,
                "maximum_weight": 20.0,
            }
        )
        self.employee = self.env["hr.employee"].create(
            {"name": "Test employee weight_control"}
        )
        self.production = self.env["mrp.production"].create(
            {
                "product_id": self.product.id,
                "product_uom_id": self.product.uom_id.id,
                "product_qty": 1.0,
            }
        )

    def test_product_logistics_fields(self):
        self.assertEqual(self.product.minimum_weight, 10.0)
        self.assertEqual(self.product.maximum_weight, 20.0)

    def test_weight_control_related_fields(self):
        wc = self.env["mrp.production.weight.control"].create(
            {
                "production_id": self.production.id,
                "weight": 15.0,
                "employee_id": self.employee.id,
            }
        )
        self.assertEqual(wc.minimum_weight, 10.0)
        self.assertEqual(wc.maximum_weight, 20.0)

    def test_is_weight_control_within_range(self):
        wc = self.env["mrp.production.weight.control"].create(
            {
                "production_id": self.production.id,
                "weight": 15.0,
                "employee_id": self.employee.id,
            }
        )
        self.assertTrue(wc.is_weight_control)

    def test_is_weight_control_below_minimum(self):
        wc = self.env["mrp.production.weight.control"].create(
            {
                "production_id": self.production.id,
                "weight": 5.0,
                "employee_id": self.employee.id,
            }
        )
        self.assertFalse(wc.is_weight_control)

    def test_is_weight_control_above_maximum(self):
        wc = self.env["mrp.production.weight.control"].create(
            {
                "production_id": self.production.id,
                "weight": 25.0,
                "employee_id": self.employee.id,
            }
        )
        self.assertFalse(wc.is_weight_control)

    def test_weight_control_ids_on_production(self):
        self.env["mrp.production.weight.control"].create(
            {
                "production_id": self.production.id,
                "weight": 15.0,
                "employee_id": self.employee.id,
            }
        )
        self.assertEqual(len(self.production.weight_control_ids), 1)

    def test_weight_control_cascade_delete(self):
        wc = self.env["mrp.production.weight.control"].create(
            {
                "production_id": self.production.id,
                "weight": 15.0,
                "employee_id": self.employee.id,
            }
        )
        self.production.unlink()
        self.assertFalse(wc.exists())
