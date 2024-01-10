{
    "name": "Custom Indogosa",
    "summary": "Adds cost field of Materials and its components.",
    "version": "16.0.1.0.0",
    "category": "Manufacture",
    "author": "Xtendoo",
    "license": "LGPL-3",
    "application": True,
    "depends": [
        "mrp",
        "base_global_discount",
    ],
    "data": [
        "views/mrp_view.xml",
        "views/product_template_view.xml",
        "views/product_pricelist_item_view.xml",
        "report/mrp_report_bom_structure_inherit.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'custom_indogosa/static/src/js/formatters.js',
            ]
    },
    "qweb": [
        "static/src/xml/mrp_bom_overview_line.xml",
    ],
    "installable": True,
}
