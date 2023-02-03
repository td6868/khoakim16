from odoo import tools
from odoo import api, fields, models

class SaleLineReport(models.Model):
    _name = "sale.line.report"
    _description = "Chi tiết báo giá"
    _auto = False
    _order = 'order_id desc'

    order_id = fields.Many2one('sale.order', string="Đơn hàng", readonly=True)
    line_type = fields.Selection([('so_line', 'Đơn hàng'),
                                ('qso_line', 'Báo giá nhanh')], string='Loại', readonly=True)
    # so_state = fields.Selection(selection=[
    #                                 ('draft', 'Báo giá'),
    #                                 ('waiting', 'Chờ duyệt'),
    #                                 ('approved', 'Đã duyệt'),
    #                                 ('sent', 'Đã gửi'),
    #                                 ('sale', 'Đơn hàng'),
    #                                 ('done', 'Đã khóa'),
    #                                 ('cancel', 'Đã hủy'),
    #                             ], string='Trạng thái', readonly=True)
    purchase_price = fields.Float(string='Chi phí', readonly=True)
    product_id = fields.Many2one('product.product', string="Sản phẩm", readonly=True)
    catg_prod_id = fields.Many2one('product.category', string="Danh mục", readonly=True)
    name = fields.Char(string='Tên sản phẩm', readonly=True)
    product_qty = fields.Float(string='Số lương', readonly=True)
    product_uom = fields.Many2one('uom.uom', string='Đơn vị', readonly=True)
    price_unit = fields.Float(string="Đơn giá", readonly=True)
    # tax_id = fields.Many2many('account.tax', string='Thuế', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Khách hàng', readonly=True)
    # price_tax = fields.Float(string='Tổng thuế', readonly=True)
    # price_subtotal = fields.Float(string='Tổng chưa thuế', readonly=True)
    # price_total = fields.Float(string='Tổng', readonly=True)
    # note = fields.Text(string="Ghi chú", readonly=True)

    def _from(self):
        return """
            FROM 
            (
                SELECT
                    qso.order_id as order_id,
                    'qso_line' as line_type,
                    qso.purchase_price as purchase_price, 
                    qso.product_id as product_id, 
                    qso.catg_prod_id as catg_prod_id,
                    qso.name as name,
                    qso.product_qty as product_qty, 
                    qso.product_uom as product_uom, 
                    qso.price_unit as price_unit,
                    qso.partner_id as partner_id
                    FROM sale_order_quick_line qso

                UNION ALL

                SELECT
                    so.order_id as order_id,
                    'so_line' as line_type,
                    so.purchase_price as purchase_price, 
                    so.product_id as product_id, 
                    so.product_uom_category_id as catg_prod_id,
                    so.name as name,
                    so.product_uom_qty as product_qty, 
                    so.product_uom as product_uom, 
                    so.price_unit as price_unit,
                    so.order_partner_id as partner_id
                    FROM sale_order_line so
            ) line
        """

    def _select(self):
        return """
            SELECT
                row_number() OVER () AS id,
                line.order_id, 
                line.line_type, 
                line.purchase_price,
                line.product_id,
                line.catg_prod_id,
                line.product_qty,
                line.price_unit,
                line.partner_id
        """

    def _group_by(self):
        return """
            GROUP BY
                line.line_type, 
                line.so_state, 
                line.purchase_price,
                line.product_id,
                line.catg_prod_id,
                line.product_qty,
                line.price_unit,
                line.tax_id,
                line.partner_id
        """

    def init(self):
        # table = 'ser_report'
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
               CREATE OR REPLACE VIEW %s AS (
                   %s
                   %s
                   %s
               )
           """ % (self._table, self._select(), self._from(), self._group_by())
        )