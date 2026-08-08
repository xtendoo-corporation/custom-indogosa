{
    "name": "Custom Indogosa",
    "summary": "Adds cost field of Materials and its components.",
    "version": "19.0.1.0.0",
    "category": "Manufacture",
    "author": "Xtendoo",
    "license": "LGPL-3",
    "application": True,
    "depends": [
        "mrp",
        "base_global_discount",
        "xtendoo_mrp_bom_cost",
        'base',
        'web',
    ],
    "data": [
        "views/mrp_view.xml",
        "views/account_tax_view.xml",
        "views/product_template_view.xml",
        "views/stock_move_line_view.xml",
    ],
    "installable": True,
}
