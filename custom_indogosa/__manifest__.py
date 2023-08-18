{
    "name": "Custom Indogosa",
    "summary": "Adds cost field of Materials and its components.",
    "version": "16.0.1.0.0",
    "category": "Manufacture",
    "author": "Xtendoo",
    "license": "LGPL-3",
    "application": True,
    "depends": ["mrp"],
    "data": [
        "views/mrp_view.xml",
        "static/src/mrp_bom_overview_line.xml",
        "report/mrp_report_bom_structure_inherit.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'custom_indogosa/static/src/js/formatters.js',
            ]
    },
    "installable": True,
}
