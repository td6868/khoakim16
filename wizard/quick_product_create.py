# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#
#############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError
from odoo.exceptions import UserError, ValidationError

class ProductAttribute(models.TransientModel):
    _name = "product.attrs.create.line"

    line_id = fields.Many2one('product.product.create')
    attribute_id = fields.Many2one('product.attribute', string="Thuộc tính", ondelete='cascade', required=True,
                                   index=True,
                                   help="The attribute cannot be changed once the value is used on at least one product.")
    value_ids = fields.Many2many('product.attribute.value', string="Giá trị", domain="[('attribute_id', '=', attribute_id)]")

class ProductProductCreate(models.TransientModel):
    _name = "product.product.create"

    prod_code = fields.Char(string='Mã sản phẩm', required=True)
    catg_prod_id = fields.Many2one('product.category', string="Danh mục", required=True)
    default_code = fields.Char(string='Mã sản phẩm', compute="_gen_product_code")

    def default_pur_price(self):
        id = self.env.context.get('active_ids')
        line = self.env['sale.order.quick.line'].browse(id)
        if line.purchase_price:
            return line.purchase_price

    purchase_price = fields.Float(string='Giá vốn', required=True, default=lambda self: self.default_pur_price() )
    attrs_line_ids = fields.One2many('product.attrs.create.line', 'line_id', 'Biến thể và thuộc tính')

    @api.depends('catg_prod_id', 'prod_code')
    def _gen_product_code(self):
        if self.catg_prod_id:
            self.default_code = '%s%s' % (self.catg_prod_id.cate_code or '', self.prod_code or '')
        else:
            self.default_code = self.prod_code or ''

    @api.onchange('prod_code')
    def action_duplicate_code(self):
        if self.prod_code:
            dup_code = self.env['product.template'].search([('prod_code', '=', self.prod_code)])
            if dup_code:
                code = self.prod_code
                self.prod_code = False
                return {
                    'warning': {
                        'title': ('Trùng sản phẩm'),
                        'message': (("Mã %s đã bị trùng với sản phẩm %s, vui lòng chọn mã khác") % (
                        code, dup_code.name))
                    },
                }

    def get_infor_product(self):
        id = self.env.context.get('active_ids')
        line = self.env['sale.order.quick.line'].browse(id)
        attrs_line = [self.attrs_line_ids.attribute_id, self.attrs_line_ids.value_ids]
        data = {
                    "sale_ok": True,
                    "purchase_ok": True,
                    "name": line.name,
                    "detailed_type": "product",
                    "invoice_policy": "order",
                    "uom_id": line.product_uom.id,
                    "uom_po_id": line.product_uom.id,
                    "categ_id": self.catg_prod_id.id,
                    "prod_code": self.prod_code,
                    "default_code": self.default_code,
                    "list_price": line.price_unit,
                    "standard_price": self.purchase_price,
                    "image_1920": line.prod_image,
                    "image_1024": line.prod_image,
                    "image_128": line.prod_image,
                    "image_256": line.prod_image,
                    "image_512": line.prod_image,
                }
        return data, line, attrs_line

    def _create_product(self, data, attrs_line):
        prod_temp = self.env['product.template']
        attrs = {
            "attribute_id": attrs_line[0].id,
            "value_ids": [(6, 0, attrs_line[1].ids)],
        }
        data["attribute_line_ids"] = [(0, 0, attrs)]
        prod_id = prod_temp.create(data)
        return prod_id

    def create_product(self):
        data, line, attrs_line = self.get_infor_product()
        prod_id = self._create_product(data, attrs_line)
        if prod_id:
            sale_order = self.env["sale.order.line"]
            vals = {
                "order_id": line.order_id.id,
                "product_template_id": prod_id.id,
                "product_id": prod_id.product_variant_id.id,
                "product_uom_qty": line.product_qty,
                "price_unit": line.price_unit,
            }
            sale_order.create(vals)
            line.update({
                "is_display": False,
                "product_id": prod_id.product_variant_id.id,
            })