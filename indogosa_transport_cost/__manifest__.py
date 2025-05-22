# __manifest__.py
{
    'name': 'Indogosa Costos de Transporte',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Gestión de costos de transporte basados en volumen',
    'author': 'Xtendoo',
    'depends': [
        'sale_management',
        'sale_margin',
        'product',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
