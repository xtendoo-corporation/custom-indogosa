{
    "name": "Weight Control",
    "summary": "Weight control",
    "version": "16.0.1.0.0",
    "category": "Product",
    "author": "Xtendoo",
    "license": "LGPL-3",
    "application": True,
    "depends": [
        'mrp',
        'product',
    ],
    "data": [
        "views/product_template_view.xml",
        "views/mrp_production_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
