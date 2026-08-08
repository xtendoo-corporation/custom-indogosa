{
    "name": "Weight Control",
    "summary": "Weight control",
    "version": "18.0.1.0.0",
    "category": "Product",
    "author": "Xtendoo",
    "license": "LGPL-3",
    "application": True,
    "depends": [
        'mrp',
        'product',
        'hr',  # employee_id (mrp.production.weight.control) depende de hr.employee,
               # dependencia real pero no declarada en el manifest de 17.0 -
               # funcionaba solo porque hr ya estaba instalado en prodequim
               # por otro motivo. Corregido al portar.
    ],
    "data": [
        "views/product_template_view.xml",
        "views/mrp_production_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
