# Copyright 2026 Xtendoo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCustomIndogosa(TransactionCase):
    def setUp(self):
        super().setUp()
        self.component = self.env["product.product"].create(
            {"name": "Component", "standard_price": 5.0}
        )
        self.finished = self.env["product.product"].create(
            {"name": "Finished product"}
        )

    def test_mrp_bom_line_total_price(self):
        bom = self.env["mrp.bom"].create(
            {
                "product_tmpl_id": self.finished.product_tmpl_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )
        line = self.env["mrp.bom.line"].create(
            {"bom_id": bom.id, "product_id": self.component.id, "product_qty": 2.0}
        )
        self.assertEqual(line.total_price, 10.0)

    def test_mrp_bom_total_bom_price(self):
        bom = self.env["mrp.bom"].create(
            {
                "product_tmpl_id": self.finished.product_tmpl_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )
        other_component = self.env["product.product"].create(
            {"name": "Other component", "standard_price": 2.0}
        )
        self.env["mrp.bom.line"].create(
            {"bom_id": bom.id, "product_id": self.component.id, "product_qty": 2.0}
        )
        self.env["mrp.bom.line"].create(
            {"bom_id": bom.id, "product_id": other_component.id, "product_qty": 3.0}
        )
        # 5.0*2 + 2.0*3 = 16.0
        self.assertEqual(bom.total_bom_price, 16.0)

    def test_account_tax_amount_default(self):
        tax = self.env["account.tax"].create({"name": "Test tax indogosa"})
        self.assertEqual(tax.amount, 0.0)

    def test_stock_move_line_partner_name_related(self):
        partner = self.env["res.partner"].create({"name": "Test partner indogosa"})
        picking_type = self.env.ref("stock.picking_type_in")
        picking = self.env["stock.picking"].create(
            {
                "partner_id": partner.id,
                "picking_type_id": picking_type.id,
                "location_id": picking_type.default_location_src_id.id
                or self.env.ref("stock.stock_location_suppliers").id,
                "location_dest_id": picking_type.default_location_dest_id.id
                or self.env.ref("stock.stock_location_stock").id,
            }
        )
        move = self.env["stock.move"].create(
            {
                "name": self.component.name,
                "product_id": self.component.id,
                "product_uom_qty": 1.0,
                "product_uom": self.component.uom_id.id,
                "picking_id": picking.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
            }
        )
        move_line = self.env["stock.move.line"].create(
            {
                "move_id": move.id,
                "product_id": self.component.id,
                "product_uom_id": self.component.uom_id.id,
                "picking_id": picking.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
            }
        )
        self.assertEqual(move_line.partner_name, partner)

    def test_product_template_logistics_fields(self):
        self.finished.product_tmpl_id.write(
            {
                "ufi": "UFI-123",
                "dun14": "DUN-456",
                "long": 1.5,
                "high": 2.5,
                "broad": 3.5,
                "weight_box": 10.0,
                "volume_box": 0.5,
                "long_box": 1.0,
                "high_box": 1.0,
                "broad_box": 1.0,
                "bottle_box": 12.0,
                "box_pallet": 20,
                "base_pallet": 1.2,
                "height_pallet": 1.8,
                "weight_pallet": 200.0,
                "volume_pallet": 1.0,
                "layers_pallet": 4.0,
            }
        )
        self.assertEqual(self.finished.product_tmpl_id.ufi, "UFI-123")
        self.assertEqual(self.finished.product_tmpl_id.box_pallet, 20)

    def test_get_volume_uom_default(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "product.volume_in_cubic_feet", False
        )
        uom = self.finished.product_tmpl_id._get_volume_uom_id_from_ir_config_parameter()
        self.assertEqual(uom, self.env.ref("uom.product_uom_cubic_meter"))

    def test_get_volume_uom_cubic_feet(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "product.volume_in_cubic_feet", "1"
        )
        uom = self.finished.product_tmpl_id._get_volume_uom_id_from_ir_config_parameter()
        self.assertEqual(uom, self.env.ref("uom.product_uom_cubic_foot"))

    def test_get_volume_uom_liters(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "product.volume_in_cubic_feet", "2"
        )
        uom = self.finished.product_tmpl_id._get_volume_uom_id_from_ir_config_parameter()
        self.assertEqual(uom, self.env.ref("uom.product_uom_litre"))

    def test_res_config_settings_default(self):
        settings = self.env["res.config.settings"].create({})
        self.assertEqual(settings.product_volume_volume_in_cubic_feet, "2")

    def test_pricelist_item_discount_onchange(self):
        discount = self.env["global.discount"].create(
            {"name": "10% off", "discount": 10.0, "discount_scope": "sale"}
        )
        item = self.env["product.pricelist.item"].new(
            {"fixed_price": 100.0, "global_discount_ids": [(6, 0, discount.ids)]}
        )
        item._onchange_global_discount_ids()
        self.assertEqual(item.price_discounted, 90.0)

    def test_pricelist_item_no_discount_onchange(self):
        item = self.env["product.pricelist.item"].new({"fixed_price": 50.0})
        item._onchange_global_discount_ids()
        self.assertEqual(item.price_discounted, 50.0)

    def test_pricelist_item_product_tmpl_profit_margin(self):
        item = self.env["product.pricelist.item"].new(
            {
                "applied_on": "1_product",
                "product_tmpl_id": self.component.product_tmpl_id.id,
                "fixed_price": 20.0,
            }
        )
        item._onchange_global_discount_ids()
        item._onchange_product_tmpl_price_cost()
        # standard_price=5.0, price_discounted=20.0 -> margin=15.0, pct=300%
        self.assertEqual(item.product_tmpl_profit_margin, 15.0)
        self.assertEqual(item.product_tmpl_profit_percentage, 300.0)

    def test_pricelist_item_product_profit_margin(self):
        item = self.env["product.pricelist.item"].new(
            {
                "applied_on": "0_product_variant",
                "product_id": self.component.id,
                "fixed_price": 20.0,
            }
        )
        item._onchange_global_discount_ids()
        item._onchange_product_price_cost()
        self.assertEqual(item.product_profit_margin, 15.0)
        self.assertEqual(item.product_profit_percentage, 300.0)
