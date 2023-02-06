# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Khoa Kim Customize',
    'version' : '1.3',
    'summary': 'Invoices & Payments',
    'sequence': 115,
    'description': """
            Module tổng hợp các tùy biến Khoa Kim ERP
    """,
    'category': 'Customize',
    'website': 'https://www.odoo.com/page/billing',
    "license": "AGPL-3",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'report/sale_order_rp.xml',
        'report/sale_order_no_img_rp.xml',
        'report/invoice_rp.xml',
        'report/stock_picking_rp.xml',
        'report/purchase_order_rp.xml',
        'report/customize_report.xml',
        'views/inherit_views.xml',
        # 'views/sale_line_report.xml',
        'wizard/invoice_so.xml',
        'wizard/quick_create_product.xml',
        'wizard/std_price_change.xml',
        'data/data.xml',
    ],
    "depends": [
        "sale",
        "base",
        "product",
        "stock",
        "stock_landed_costs",
        "report_xlsx",
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
