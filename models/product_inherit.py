# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import ssl
from vietnam_number import n2w
import string
import random
import math
from woocommerce import API
from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError
from odoo.tools import config
import requests
from datetime import timedelta
import base64
import urllib.request
import gspread
import time
# from gspread.cell import Cell
#
# INFO = {
#           "type": "service_account",
#           "project_id": "gsodsync",
#           "private_key_id": "23521eba50f0f7e57f857777fb40dbc40a0227dc",
#           "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDQ3Pkn7iuLvfj1\nQ3Q9IRYj847mxCzQM+vxCQxFN0q8zISwf3C0AWvoacDc/XmMaRLd5bno3Eg3NmFi\nt1JePA7yszZ0eBX5+EvNgoLCafmSVeWMZyyV4C92bqu8QZ/MXe7go+6Nn1z4khni\nXKquyj1k/XJj+hZJQ5H5hsCDEKwFxKcAKEn4XzBYer+bntjcBrvt0BW9A/QiB/nY\niqQvu+QwZ11bTsK6felHLayzeckgzeh99JWR7GKnOMvXcujh6F2igzAlrkr1SeV3\nKWLQ8I8zF7vSPxQziSztlDWnzH5Twa2zqsoSa/STB2kFjikBGKDiaiXny+EHl2YL\nmhgW8jzhAgMBAAECggEALDTI62Gmh9Iykj6vqIyLMhrHwSH+VibXJlIC7ddxExq6\nbtzaTs8KNsvDTUK86jIHEz4fJiERi9YPsKQaY+WUSFwUB3yvMhQSfzHDWUCy2P0j\nM59WuXYUtZ1g7dx55Phwqc0onYMAW4AYyGdSnOIjMm/OOUjiVKlfiQ+zSUpLDoEZ\n2Ua1wCaLsWqPtKMZjhM3M8jupCLjZBV38DhoRN/ykj5Cn4XGq54O5ZYRLswDhkYP\nHxCH3XrzahdrYv0B2dLMru8HOhs75wbNYDwY9NV9cqtWKnBHHuqcIeGlXiPwH+4J\ngVfVcPDb46ilXJahPrc8GQRktXf3LHMpQKfA8GEz/QKBgQDxnjPJAkRL1AvTKO3o\nBoj2RhlUAYvNhClR/VsCEAsA7VUWR5AMXxdEjSsMPWXnLorQgWw9duz0StMA1R7N\nV+xtbrPzi+Om1fl3+LspqWgHCr9eu9bcveSFuFtd+arcNEyhtV3thI82hcZab0J0\nfm1igWSR+DMWKXsOoOfqTutczwKBgQDdS6Z0LJAEDxY5Ep0whYbUKU7OVhm4rRkt\ntAQ8GFdxXi+f8he9SgVHn7FoP1pJEma5eOAjuk+3NH/TRQ6uD/948jRfEtpYx/Mz\nPyyEZl3y/r/1eyFo9E9i98S21TcOOIRk3ozQlJyObSPzrJvhS9P15gYB5eBtB+Nt\n6vHuu+YXTwKBgQDrOaSaze0lkZPNiKxM1ofikw43faXYeBEuNCS01l+QEH5kyVjQ\n4oapg3HkYaXisqoMIeP51t0LXAkeZ12sdivDwiHJOmhwVSKhDPNRtQ6ExI7YsLCW\niPyAvqGc1OLlrLjqOcLu6L3wS7527phZB3iAjQ4XGfbKXani7P27XAfBewKBgQDN\nHVaOrdNa/8TgZ6FtHQbI1fTmiaXTqBYDZ6zZKtK6EMvh29onKFnWdm1QrA/6VOUE\nGsbeNs22iSHF6Gdf7RIlv5HNYcMisUp5gJ+5pMyF85xnY5anGnQOzor10JD0TGxi\ntmkc1/J4jS7aqG3fmJJBhNCip7iqNrqV4kQWvPDbPwKBgG1TjB99rHM6WY3GoBHd\nz6FJcdJXRpjYpEKE2nWHt8rec9P61fYIrYnk/4zWHm0kbQlMxUbVoaiuzhAa0XcH\nge3VJpBmjvOqJDtcV7EyOadAIw6HgXSeKUwosvl/o4l/v7ByDFkuth4tLE3Fo7Sg\nCK5m9S/urxMLC9As8J45S21q\n-----END PRIVATE KEY-----\n",
#           "client_email": "odoogsheetkk@gsodsync.iam.gserviceaccount.com",
#           "client_id": "116816502838220913532",
#           "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#           "token_uri": "https://oauth2.googleapis.com/token",
#           "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#           "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/odoogsheetkk%40gsodsync.iam.gserviceaccount.com"
#         }
# SA = gspread.service_account_from_dict(INFO)
# WB = SA.open("SyncOdooProd")
# WS_PROD = WB.worksheet("MasterProd")
# WS_CATG = WB.worksheet("MasterCatg")

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

class Pricelist(models.Model):
    _inherit = 'product.pricelist'

    type_pl = fields.Selection([
        ('main', 'B???ng gi?? ni??m y???t'),
        ('policy', 'Theo ch??nh s??ch'),
        ('non_policy', 'Kh??ng theo ch??nh s??ch')
    ], string="Lo???i b???ng gi??", default='main', required=True)
    # def_pl_id = fields.Many2one('product.pricelist', string="B???ng gi?? NY", domain=[('type_pl', '=', 'main')])
    # user_id = fields.Many2one('res.user', string="Nh??n vi??n kinh doanh")
    discount = fields.Float(string='Chi???t kh???u theo b???ng gi?? (%)', tracking=True)
    roles = fields.Selection([
        ('daily1', '?????i l?? c???p 1'),
        ('daily2', '?????i l?? c???p 2'),
        ('daily3', '?????i l?? c???p 3'),
        ('customer', 'Kh??ch h??ng l???'),
    ], string='C???p ?????i l??', default='customer', required=True)
    count_pl = fields.Integer(string='S??? l?????ng SP', compute='count_all_pl')

    # def write(self, vals):
    #     super(Pricelist, self).write(vals)

    def action_view_pricelist(self):
        self.ensure_one()
        view_id = self.env.ref('khoakim_customize.view_price_list_item_kk')
        search_view_id = self.env.ref('khoakim_customize.view_price_list_item_filter_kk')
        result = {
                    "name": "B???ng gi?? chi ti???t",
                    "res_model": "product.pricelist.item",
                    "type": "ir.actions.act_window",
                    'view_mode': 'tree',
                    "context": {"create": False},
                    "domain": [('pricelist_id.id', '=', self.id)],
                    "view_id": view_id.ids,
                    "search_view_id": search_view_id.ids,
                }
        return result

    def count_all_pl(self):
        count = self.env['product.pricelist.item'].search_count([('pricelist_id.id', '=', self.id)])
        self.count_pl = count

class AccountMove(models.Model):
    _inherit = "account.move"

    priority_so = fields.Selection(selection=[
        ('1', 'B??nh th?????ng'),
        ('2', '??u ti??n'),
    ], string='M??c ????? ??u ti??n', default='1', tracking=True)
    shipping_method = fields.Char(string="Ph????ng th???c v???n chuy???n", tracking=True)
    pst_by_word = fields.Char(string="S??? ti???n b???ng ch???")

    # ap dung thue, lam tron, stt
    def apply_all_line(self):
        i = 1
        for line in self.invoice_line_ids:
            line.write({
                'seq_cus': i,
            })
            i += 1

    @api.constrains('amount_total')
    def _compute_subtotal_word(self):
        if self.amount_total:
            pst_word = n2w(str(self.amount_total/10))
            self.pst_by_word = pst_word.capitalize() + ' ?????ng'
        else:
            self.pst_by_word = ''

    @api.model
    def create(self, vals):
        rec = super(AccountMove, self).create(vals)
        self.apply_all_line()
        return rec

    def write(self, vals):
        rec = super(AccountMove, self).write(vals)
        self.apply_all_line()
        return rec

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    seq_cus = fields.Integer(string="STT", readonly=True)
    note = fields.Text(string="Ghi ch??")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    url_img = fields.Char(string="URL ???nh 1")
    default_code = fields.Char(string="M?? n???i b???", compute="_gen_product_code")
    wp_ok = fields.Boolean(string="Kh??? d???ng ??? website")
    prod_code = fields.Char(string="M?? SP/NSX", required=True)
    display_name = fields.Char(string="T??n hi???n th???", compute="_new_display_name")
    sale_ok = fields.Boolean('C?? th??? b??n', default=False)
    purchase_ok = fields.Boolean('C?? th??? mua', default=False)
    appr_state = fields.Boolean('Tr???ng th??i duy???t', default=False)
    url_img2 = fields.Char(string="URL ???nh 2")
    url_img3 = fields.Char(string="URL ???nh 3")
    url_img4 = fields.Char(string="URL ???nh 4")
    url_img5 = fields.Char(string="URL ???nh 5")
    # product_ok = fields.Boolean('L?? s???n ph???m', default=False)

    product_attr_tags = fields.Many2many("product.template.attr.value",
                                         string="Gi?? tr??? thu???c t??nh",
                                         required=True)

    @api.depends('name', 'product_attr_tags')
    def _new_display_name(self):
        display_name = ''
        for rec in self:
            if rec.name:
                display_name = rec.name
                if rec.product_attr_tags:
                    display_name = display_name + " ( "
                    for tag in rec.product_attr_tags:
                        display_name += tag.name + " "
                    display_name = display_name + ")"
            rec.display_name = display_name

    def purchase_create_temp(self):
        if self.env.company.purc_comp_id:
            data = {
                "name": self.env.company.purc_comp_id.id,
                "min_qty": 1.0,
                "price": self.standard_price,
                "sequence": 1,
                "product_tmpl_id": self.id,
            }
            self.update({
                "seller_id": data,
            })

    def _get_qty_available(self):
        self.ensure_one()
        qty_available = self.qty_available
        uom_name = self.uom_id.name
        return {
            'qty_available': qty_available,
            'uom_name': uom_name
        }

    # def change_name(self):

    @api.constrains("prod_code", "categ_id", "product_attr_tags")
    def _gen_product_code(self):
        for prod in self:
            default_code = prod.prod_code or ''

            if prod.categ_id:
                default_code = '%s%s' % (prod.categ_id.cate_code or '', prod.prod_code or '')
            try:
                for tag in prod.product_attr_tags:
                    default_code += '%s' % (tag.acode)
            except:
                pass
            prod.default_code = default_code

    # @api.onchange('url_img')
    # def onchange_image(self):
    #     if self.url_img:
    #         context = ssl._create_unverified_context()
    #         get_img = urllib.request.urlopen(self.url_img, context=context).read()
    #         img_b64 = base64.b64encode(get_img)
    #         self.write({
    #             "image_1920": img_b64,
    #             "image_1024": img_b64,
    #             "image_128": img_b64,
    #             "image_256": img_b64,
    #             "image_512": img_b64,
    #         })

    def check_perm_product_temp(self):
        group_pass = 'khoakim_customize.group_approval_product_temp'
        user_id = self.env.user
        if user_id.has_group(group_pass):
            return True
        return False

    def prod_temp_approvaled(self):
        check_perm = self.check_perm_product_temp()
        if check_perm:
            for p in self:
                p.write({
                    'sale_ok': True,
                    'purchase_ok': True,
                    'appr_state': True,
                })
        else:
            return {
                'warning': {
                    'title': ('L???i ng?????i d??ng'),
                    'message': (("Ng?????i d??ng kh??ng ???????c quy???n truy c???p"))
                },
            }

    def prod_temp_approvaled_batch(self):
        for p in self.browse(self.env.context['active_ids']):
            p.prod_temp_approvaled()

    def prod_temp_deny_batch(self):
        check_perm = self.check_perm_product_temp()
        if check_perm:
            for p in self.browse(self.env.context['active_ids']):
                p.prod_temp_deny()
        else:
            return {
                'warning': {
                    'title': ('L???i ng?????i d??ng'),
                    'message': (("Ng?????i d??ng kh??ng ???????c quy???n truy c???p"))
                },
            }

    def prod_temp_deny(self):
        check_perm = self.check_perm_product_temp()
        if check_perm:
            for p in self:
                p.write({
                    'active': False,
                    'sale_ok': False,
                    'purchase_ok': False,
                    'appr_state': False,
                         })
        else:
            return {
                'warning': {
                    'title': ('L???i ng?????i d??ng'),
                    'message': ("Ng?????i d??ng kh??ng ???????c quy???n truy c???p")
                },
            }

    def check_duplicate_tags(self, attrs):
        for attr in attrs:
            if (attrs.count(attr) > 1):
                return attr
        return False

    @api.onchange('product_attr_tags')
    def action_check_duplicate_code(self):
        for rec in self:
            if rec.product_attr_tags:
                attrs = []
                for tag in rec.product_attr_tags:
                    attrs.append(tag.attr_id)
                check = rec.check_duplicate_tags(attrs)
                if check:
                    return {
                                'warning': {
                                    'title': ('L???i khai b??o s???n ph???m'),
                                    'message': (_("Vui l??ng ki???m tra thu???c t??nh %s ???? xu???t hi???n") % (check.name))
                                    },
                            }

    @api.model
    def create(self, vals):
        rec = super(ProductTemplate, self).create(vals)
        # if self.wp_ok == True:
        #     self.update_product_wp()
        check_pass = self.check_perm_product_temp()
        if check_pass:
            self.write({'appr_state': True})
        # self._gen_product_code()
        return rec

    def write(self, vals):
        rec = super(ProductTemplate, self).write(vals)
        return rec

# class ProductAttributeValues(models.Model):
#     _inherit = 'product.attribute.value'
#
#     acode = fields.Char(string='M?? bi???n th???', required=True)
#     attr_term_wp = fields.Char(string='ID')

# class ProductAttribute(models.Model):
#     _inherit = 'product.attribute'
#
#     attr_wp = fields.Char(string='ID')

class ProductCategory(models.Model):
    _inherit = 'product.category'

    ccode = fields.Char(string="M?? nh??m s???n ph???m", required=True)
    cate_code = fields.Char(string="M?? nh??m", compute='_gene_code_cate', store=True)
    url_img = fields.Char(string="URL ???nh")
    wp_ok = fields.Char(string="Kh??? d???ng tr??n website")
    cate_id = fields.Integer(string="ID WP")

    @api.depends('ccode', 'parent_id')
    def _gene_code_cate(self):
        for cate in self:
            if cate.parent_id:
                cate.cate_code = '%s%s' % (cate.parent_id.cate_code or '', cate.ccode or '')
            else:
                cate.cate_code = cate.ccode or ''

    @api.onchange('ccode')
    def action_duplicate_categ_code(self):
        if self.ccode:
            dup_code = self.env['product.category'].search([('ccode', '=', self.ccode)])
            if dup_code:
                code = self.ccode
                self.ccode = False
                return {
                            'warning': {
                                'title': ('Tr??ng nh??m s???n ph???m'),
                                'message': (("M?? %s ???? b??? tr??ng v???i nh??m s???n ph???m %s, vui l??ng ch???n m?? kh??c") % (code, dup_code.name))
                            },
                        }

    #Update gsheet
    def update_catg_gsheet(self, catg_ids):
        # time_update = fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # for rec in catg_ids:
        #     if rec.wp_ok:
        #         cell = WS_CATG.find(query=str(rec.id), in_row=2)
        #         vals = [time_update, rec.id, rec.name, rec.ccode, rec.parent_id.name]
        #         if cell:
        #             row = cell.row
        #         else:
        #             row = next_available_row(WS_CATG)
        #         cells = []
        #         for i in range(len(vals)):
        #             cells.append(Cell(row=int(row), col=i + 1, value=vals[i]))
        #         WS_CATG.update_cells(cells)
        #         time.sleep(2)
        return True

    # ?????ng b??? ho?? gsheet
    def sync_odoo_catg_gsheet(self):
        catg_ids = self.browse(self.env.context['active_ids'])
        self.update_catg_gsheet(catg_ids=catg_ids)

    # authen wp
    def wp_auth(self):
        com_id = self.env.company or self.env['res.company'].search([('wp_url', '=', True),
                                                                     ('woo_ck', '=', True),
                                                                     ('woo_cs', '=', True)], order='id asc', limit=1)
        wp_url = com_id.wp_url
        woo_ck = com_id.woo_ck
        woo_cs = com_id.woo_cs
        if (wp_url == False or woo_ck == False or woo_cs == False):
            return False
        wcapi = API(
            url=wp_url,
            consumer_key=woo_ck,
            consumer_secret=woo_cs,
            version="wc/v3",
            timeout=30
        )
        return wcapi

    # check category id create and update
    def check_categ_wp(self, wcapi):
        data = {
            "name": self.name,
            "parent": self.parent_id.cate_id or 0,
            "image": self.url_img or "",
            "description": "",
        }
        if self.sku_wp:
            update = wcapi.put("products/categories/" + str(self.cate_id), data)
        else:
            update = wcapi.post("products/categories", data)
        status = update.status_code
        if status == 201:
            js = update.json()
            self.cate_id = js['id']
        return self.cate_id

    #?????ng b??? danh m???c
    def sync_categ_product_wp(self):
        wcapi = self.wp_auth()
        if wcapi:
            for p in self.browse(self.env.context['active_ids']):
                if p.wp_ok:
                    p.check_categ_wp(wcapi)

    # ?????ng b??? t??? ?????ng
    def auto_sync_category_wp(self):
        wcapi = self.wp_auth()
        if wcapi:
            categ_ids = self.env['product.category'].search([], order='id asc')
            for rec in categ_ids:
                rec.check_categ_wp(wcapi)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_attr_tags = fields.Many2many("product.template.attr.value",
                                         related="product_tmpl_id.product_attr_tags",
                                         string="Gi?? tr??? thu???c t??nh")
    display_name = fields.Char(string="T??n hi???n th???", related="product_tmpl_id.display_name")

    def _get_qty_available(self):
        self.ensure_one()
        qty_available = self.qty_available
        uom_name = self.uom_id.name
        return {
            'qty_available': qty_available,
            'uom_name': uom_name
        }

#     prod_code = fields.Char(string="M?? SP/SX", compute='_get_temp_prod')
#     default_code = fields.Char(string="M?? n???i b???", compute='_gen_product_attrs_code', store=True)
#     sku_wp = fields.Char(string="ID WP")
#     extra_price = fields.Float(string="Gi?? ni??m y???t", default=0)
#     is_change_ep = fields.Boolean(default=False)
#
#     @api.model
#     def create(self, vals):
#         res = super(ProductProduct, self).create(vals)
#         self.purchase_create()
#         return res
#
#     def write(self, vals):
#         res = super(ProductProduct, self).write(vals)
#         try:
#             if self.is_change_ep:
#                 self.check_price_extra(vals["extra_price"])
#                 self.is_change_ep = False
#         except:
#             pass
#         return res
#
#     def purchase_create(self):
#         if self.env.company.purc_comp_id:
#             data = {
#                 "name": self.env.company.purc_comp_id.id,
#                 "min_qty": 1.0,
#                 "price": self.standard_price,
#                 "sequence": 1,
#                 "product_tmpl_id": self.id,
#             }
#             self.update({
#                 "seller_id": data,
#             })
#
#     @api.onchange("extra_price")
#     def onchange_extra_price(self):
#         if self.extra_price:
#             self.is_change_ep = True
#
#     def check_price_extra(self, extra_price):
#         df_pl = self.env['product.pricelist'].search([('type_pl','=','main')], limit=1)
#         pl_item = self.env['product.pricelist.item']
#         prod_price = pl_item.search([('pricelist_id', '=', df_pl.id),
#                                     ('product_tmpl_id', '=', self.id)], limit=1)
#         if prod_price:
#             if extra_price:
#                 prod_price.write({'fixed_price': extra_price})
#             else:
#                 self.extra_price = prod_price.fixed_price
#         else:
#             prod_temp = self.product_tmpl_id
#             prod_id = self.env['product.product'].search([('id', '=', self.id)])
#             vals = {
#                         "applied_on": "0_product_variant",
#                         "pricelist_id": df_pl.id,
#                         "product_tmpl_id": prod_temp.id,
#                         "product_tmpl_id": prod_id.id,
#                         "fixed_price": extra_price,
#                     }
#             pl_item.create(vals)
#
#     def update_extra_price_batch(self):
#         for p in self.browse(self.env.context['active_ids']):
#             p.check_price_extra(p.extra_price)
#
#     def _get_temp_prod(self):
#         for p in self:
#             if p.product_tmpl_id:
#                 p.prod_code = p.product_tmpl_id.prod_code or ''
#
#     @api.depends('product_template_attribute_value_ids', 'prod_code', 'product_tmpl_id.default_code')
#     def _gen_product_attrs_code(self):
#         for prod in self:
#             code = prod.product_tmpl_id.default_code or ''
#             attrs = prod.product_template_attribute_value_ids
#             if attrs:
#                 b = []
#                 for s in attrs:
#                     b.append((s.attribute_id.sequence, s.product_attribute_value_id.acode))
#                 d = sorted(b)
#                 for c in d:
#                     code += c[1] or ''
#                 prod.default_code = code
#
#     @api.onchange('url_img')
#     def onchange_image(self):
#         if self.url_img:
#             get_img = urllib.request.urlopen(self.url_img).read()
#             img_b64 = base64.b64encode(get_img)
#             self.write({
#                 "image_1920": img_b64,
#                 "image_1024": img_b64,
#                 "image_128": img_b64,
#                 "image_256": img_b64,
#                 "image_512": img_b64,
#                 "image_variant_1920": img_b64,
#                 "image_variant_1024": img_b64,
#                 "image_variant_512": img_b64,
#                 "image_variant_256": img_b64,
#                 "image_variant_128": img_b64,
#             })
#
#     def compute_variant_product(self, tag=None):
#         attrs = ''
#         name = self.name
#         attr_prod = self.product_template_attribute_value_ids
#         tags = []
#         brand = 'Kh??ng c??'
#         for a in attr_prod:
#             if a.attribute_id.sequence == 0:
#                 brand = a.name
#             attrs += '<p>' + a.attribute_id.name + ' : ' + a.name + '</p>'
#             name += ' ' + a.name
#             if tag == True:
#                 tags.append({"name": a.name})
#         return {'brand': brand, 'attrs': attrs, 'name': name, 'tags': tags}
#
#     # ?????ng b??? ho?? gsheet
#     def sync_odoo_prod_gsheet(self):
#         prod_ids = self.browse(self.env.context['active_ids'])
#         time_update = fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         for rec in prod_ids:
#             cell = WS_PROD.find(query=str(rec.id), in_column=2)
#             variants = self.compute_variant_product()
#             vals = [time_update, rec.id, rec.url_img or '', rec.url_img or rec.product_tmpl_id.url_img or '', variants['name'], rec.prod_code, rec.categ_id.name, variants['brand'], variants['attrs'], rec.list_price, rec.virtual_available]
#             if cell:
#                 row = cell.row
#             else:
#                 row = next_available_row(WS_PROD)
#             # WS_PROD.update_cell(values=vals, row=int(row))
#             cells = []
#             for i in range(len(vals)):
#                 cells.append(Cell(row=int(row), col=i + 1, value=vals[i]))
#             WS_PROD.update_cells(cells)
#             time.sleep(2)
#
#     #get pricelist product
#     def get_all_product_list(self):
#         prod_prices = self.env['product.pricelist.item'].search(['|',('product_tmpl_id', '=', self.id),
#                                                                  ('applied_on', '=', '3_global'),
#                                                                  ('pricelist_id.type_pl', '=', 'policy')]
#                                                                 )
#         main_price = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', self.id),
#                                                                  ('pricelist_id.type_pl', '=', 'main')],
#                                                                limit=1)
#         price_main = main_price.fixed_price or self.list_price
#         all_pu = {'main': price_main,}
#         for pl in prod_prices:
#             if (pl.applied_on == '3_global' and pl.price):
#                 pl_roles = pl.pricelist_id.roles
#                 price_policy = price_main - (pl.price_discount / 100 * price_main) + pl.price_surcharge
#                 if pl.price_round:
#                     price_policy = math.ceil(price_policy/pl.price_round) * pl.price_round
#                 all_pu.update({pl_roles: price_policy,})
#         return all_pu
#
#     #authen wp
#     def wp_auth(self):
#         com_id = self.env.company or self.env['res.company'].search([('wp_url', '=', True),
#                                                                      ('woo_ck', '=', True),
#                                                                      ('woo_cs', '=', True)], order='id asc', limit=1)
#         wp_url = com_id.wp_url
#         woo_ck = com_id.woo_ck
#         woo_cs = com_id.woo_cs
#         if (wp_url == False or woo_ck == False or woo_cs == False):
#             return False
#         wcapi = API(
#             url=wp_url,
#             consumer_key=woo_ck,
#             consumer_secret=woo_cs,
#             version="wc/v3",
#             timeout=30
#         )
#         return wcapi
#
#     #create wp product
#     def update_wp_product(self, categ_id, wcapi):
#         variants = self.compute_variant_product(tag=True)
#         prices = self.get_all_product_list()
#         stock_quan = self.qty_available or 12
#         src = [self.url_img or self.product_tmpl_id.url_img, self.url_img2, self.url_img3, self.url_img4, self.url_img5]
#         images = []
#         for s in src:
#             if s:
#                 images.append({"src": s})
#
#         status = 'private'
#         if self.product_tmpl_id.wp_ok:
#             status = 'publish'
#
#         data = {
#                     "name": variants['name'],
#                     "type": "simple",
#                     "status": status,
#                     "regular_price": str(prices['main']),
#                     "description": "",
#                     "short_description": variants['attrs'],
#                     "sku": str(self.default_code),
#                     "manage_stock": 1,
#                     "stock_quantity": str(stock_quan),
#                     "categories": [
#                         {
#                             "id": int(categ_id)
#                         },
#                     ],
#                     "images": images,
#                     "tags": variants['tags'],
#                     "meta_data": [
#                         {
#                             "key": "_pricing_rules",
#                             "value": {
#                                 "set_1": {
#                                     "conditions_type": "all",
#                                     "conditions": {
#                                         "1": {
#                                             "type": "apply_to",
#                                             "args": {
#                                                 "applies_to": "roles",
#                                                 "roles": [
#                                                     "daily1"
#                                                 ]
#                                             }
#                                         }
#                                     },
#                                     "collector": {
#                                         "type": "product"
#                                     },
#                                     "mode": "continuous",
#                                     "rules": {
#                                         "1": {
#                                             "from": "1",
#                                             "type": "fixed_price",
#                                             "amount": str(prices["daily1"] or 0)
#                                         }
#                                     },
#                                 },
#                                 "set_2": {
#                                     "conditions_type": "all",
#                                     "conditions": {
#                                         "1": {
#                                             "type": "apply_to",
#                                             "args": {
#                                                 "applies_to": "roles",
#                                                 "roles": [
#                                                     "daily2"
#                                                 ]
#                                             }
#                                         }
#                                     },
#                                     "collector": {
#                                         "type": "product"
#                                     },
#                                     "mode": "continuous",
#                                     "rules": {
#                                         "1": {
#                                             "from": "1",
#                                             "type": "fixed_price",
#                                             "amount": str(prices["daily2"] or 0)
#                                         }
#                                     },
#                                 },
#                                 "set_3": {
#                                     "conditions_type": "all",
#                                     "conditions": {
#                                         "1": {
#                                             "type": "apply_to",
#                                             "args": {
#                                                 "applies_to": "roles",
#                                                 "roles": [
#                                                     "daily3"
#                                                 ]
#                                             }
#                                         }
#                                     },
#                                     "collector": {
#                                         "type": "product"
#                                     },
#                                     "mode": "continuous",
#                                     "rules": {
#                                         "1": {
#                                             "from": "1",
#                                             "type": "fixed_price",
#                                             "amount": str(prices["daily3"] or 0)
#                                         }
#                                     },
#                                 }
#                             }
#                         }
#                     ],
#                 }
#         if self.sku_wp:
#             update = wcapi.put("products/" + str(self.sku_wp), data)
#         else:
#             update = wcapi.post("products", data)
#         status = update.status_code
#         if status == 201:
#             js = update.json()
#             self.sku_wp = js['id']
#         return self.sku_wp
#
#     #?????ng b??? ho?? s???n ph???m web
#     def sync_product_wp(self):
#         wcapi = self.wp_auth()
#         if wcapi:
#             categ_id = self.categ_id.check_categ_wp(wcapi)
#             self.update_wp_product(wcapi=wcapi, categ_id=categ_id)
#
#     #batch ?????ng b??? s???n ph???m
#     def batch_sync_product_wp(self):
#         for p in self.browse(self.env.context['active_ids']):
#             p.sync_product_wp()
#
#     #?????ng b??? t??? ?????ng
#     def auto_sync_product_wp(self):
#         prod_ids = self.env['product.product'].search([('detailed_type', '=', 'product')],
#                                                       order='id asc')
#         for rec in prod_ids:
#             rec.sync_product_wp()

class ResPartnerCustomize(models.Model):
    _inherit = 'res.partner'

    phone = fields.Char(string="S??? ??i???n tho???i", required=True)
    roles = fields.Selection([
        ('daily1', '?????i l?? c???p 1'),
        ('daily2', '?????i l?? c???p 2'),
        ('daily3', '?????i l?? c???p 3'),
        ('customer', 'Kh??ch h??ng l???')
    ], string='C???p ?????i l??', default='customer', required=True)
    wp_user = fields.Char(string="T??i kho???n portal")
    wp_password = fields.Char(string="M???t kh???u portal")
    type_vend = fields.Boolean(string="NCC TQ")
    vend_code = fields.Char(string="M?? phi???u GH")

    @api.onchange('phone')
    def action_duplicate_customer(self):
        res_partner = self.env['res.partner']
        if self.phone:
            dup_phone = res_partner.search_count([('phone', '=', self.phone)])
            if dup_phone:
                phone = self.phone
                partner = res_partner.search([('phone', '=', self.phone)]).name
                self.write({'phone': False})
                return {
                    'warning':  {
                                    'title': ('Tr??ng s??? ??i???n tho???i'),
                                    'message': (("S??? %s ???? b??? tr??ng v???i kh??ch %s, vui l??ng ki???m tra l???i kh??ch h??ng") % (phone, partner)),
                                 },
                }

    @api.onchange('name', 'roles')
    def action_def_pricelist(self):
        if self.name:
            pl = self.env['product.pricelist']
            def_pl = pl.search([('type_pl', '=', 'main')], limit=1)
            if self.roles:
                pl = pl.search([('roles', '=', self.roles)], limit=1)
                if pl:
                    def_pl = pl
            self.property_product_pricelist = def_pl.id

    def action_view_price_history_respartner(self):
        self.ensure_one()
        view_id = self.env.ref('khoakim_customize.view_sale_order_line_history_kk')
        search_view_id = self.env.ref('khoakim_customize.view_sale_order_line_filter_kk')
        result = {
                    "name": "L???ch s??? gi??",
                    "res_model": "sale.order.line",
                    "type": "ir.actions.act_window",
                    "view_mode": "tree",
                    "domain": ['|', '|' , ('order_partner_id', '=', self.id), ('order_partner_id.parent_id', '=', self.id), ('order_partner_id.parent_id', '=', self.parent_id.id)],
                    "context": {"create": False},
                    "view_id": view_id.ids,
                    "search_view_id": search_view_id.ids,
                }
        return result

    def create_acc_distributor(self):
        com_id = self.env.company or self.env['res.company'].search([('wp_url', '=', True),
                                                                     ('woo_ck', '=', True),
                                                                     ('woo_cs', '=', True)],
                                                                    order='id asc', limit=1)
        wp_user = com_id.wp_user
        wp_pass = com_id.wp_pass
        c = string.ascii_lowercase + string.ascii_uppercase + string.digits
        username = ''
        password = ''

        if (com_id.wp_url or wp_user or wp_pass):
            wp_url = com_id.wp_url + '/wp-json/wp/v2/users'

            if self.phone:
                if self.email:
                    email = self.email
                else:
                    email = self.phone + '@khoakim.com.vn'
                username = str(self.phone)[0:6] + random.choice(c)
                password = str(self.phone) + random.choice(c)

            if self.roles:
                data = {
                    "username": username,
                    "password": password,
                    "name": self.name,
                    "email": email,
                    "roles": self.roles,
                }
                r = requests.post(wp_url, auth=(wp_user, wp_pass), json=data)
                if (r.status_code == '201'):
                    self.write({
                        'wp_user': username,
                        'wp_password': password,
                    })
                    return {
                        'warning': {
                            'title': ('T???o t??i kho???n th??nh c??ng'),
                            'message': (("T??i kho???n c???a kh??ch h??ng ???? ???????c t???o th??nh c??ng! V???i t??n t??i kho???n l?? %s v?? m???t kh???u l?? %s") % (username, password))
                        },
                    }
                else:
                    return {
                        'warning': {
                            'title': ('???? c?? l???i'),
                            'message': (("???? c?? l???i %s . Li??n h??? v???i admin ????? gi???i ????p!") % (r.status_code)),
                        },
                    }
            else:
                return {
                    'warning': {
                        'title': ('???? c?? l???i'),
                        'message': (("Ch??a c???p nh???t ch??nh s??ch ?????i l?? cho kh??ch h??ng n??y!")),
                    }
                }
        return UserError('L???i ch??a c?? th??ng tin v??? website ?????i l??. H??y v??o c??ng ty ????? khai b??o!')

    # def reset_wp_password(self):
    #     com_id = self.env.company
    #     wp_user = com_id.wp_user
    #     wp_pass = com_id.wp_pass
    #
    #     if (com_id.wp_url or wp_user or wp_pass):
    #         wp_url = com_id.wp_url + '/wp-json/wp/v2/users'

class PurchaseTags(models.Model):
    _name = 'purchase.tags'
    _description = 'Th??? mua h??ng'

    name = fields.Char(string="T??n th???", required=True)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vend_name = fields.Char(string='M?? phi???u TQ')
    tag_ids = fields.Many2many('purchase.tags', string='Th???')
    state_stock_move = fields.Selection([
        ('to_do', 'Ch??? nh???p kho'),
        ('done', 'Ho??n th??nh'),
        ('return', 'Tr??? h??ng')
    ], string='Tr???ng th??i nh???p kho', compute="_compute_state_stock_move")

    def seq_vendor_purchase(self, vals):
        partner_id = vals['partner_id']
        name_vend = self._check_vendor_purchase(partner_id)
        if name_vend:
            if 'company_id' in vals:
                vals['vend_name'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code('name.vendor') or _('M???i')
            else:
                vals['vend_name'] = self.env['ir.sequence'].next_by_code('name.vendor') or _('M???i')
        return False

    # ap dung thue, lam tron, stt
    def apply_all_line(self):
        i = 1
        for line in self.order_line:
            line.write({
                'seq_cus': i,
            })
            i += 1

    def _check_vendor_purchase(self, p_id):
        partner_id = self.env['res.partner'].search([('id', '=', p_id)])
        if partner_id.type_vend and partner_id.vend_code:
            return True
        return False

    def _compute_state_stock_move(self):
        picking = self.env["stock.picking.type"].search([("code", "=", "incoming")], limit=1)
        return_type = picking.return_picking_type_id.id
        for rec in self:
            if rec.picking_ids:
                for sp_id in rec.picking_ids:
                    if sp_id.picking_type_id.id == return_type:
                        rec.state_stock_move = 'return'
                        return True
                    if sp_id.state not in ['cancel', 'done']:
                        rec.state_stock_move = 'to_do'
                    else:
                        rec.state_stock_move = 'done'
            else:
                rec.state_stock_move = False

    def get_selection_label(self, object, field_name, field_value):
        return _(dict(self.env[object].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

    def update_order_line_vendor(self, data):
        line = self.order_line.filtered(lambda l: l.id == data[0])
        name = self.env['res.users'].search([('id', '=', data[3])]).name
        time = fields.Datetime.now()
        wt = 0

        if data[2] == 'ordering':
            wt = int(data[1])+10
        if data[2] == 'picking':
            wt = 7
        if data[2] == 'done':
            wt = 3

        date_planed = fields.Date.today() + timedelta(days=wt)
        status = self.get_selection_label(object='purchase.order.line',
                                          field_name='status_order',
                                          field_value=data[2])

        status_order = self.get_selection_label(object='purchase.order.line',
                                          field_name='status_order',
                                          field_value=line.status_order)

        message = name + " : " + status_order + " => "+ status + " - " + str(time)
        line.update({
            "status_order": data[2],
            "date_planed": date_planed,
            "update_log": message
        })

    @api.model
    def create(self, vals):
        rec = super(PurchaseOrder, self).create(vals)
        self.seq_vendor_purchase(vals)
        self.apply_all_line()
        return rec

    def write(self, vals):
        rec = super(PurchaseOrder, self).write(vals)
        self.apply_all_line()
        return rec

    # t??nh seq cho phi???u mua c??ng vendor
    # def _compute_vendor_purchase(self, p_id):
    #     partner_id = self.env['res.partner'].search([('id', '=', p_id)])
    #     if partner_id.type_vend and partner_id.vend_code:
    #         vend_code = partner_id.vend_code
    #         po = self.env['purchase.order']
    #         num_po = po.search_count([('partner_id', '=', partner_id.id)]) + 1
    #         name = vend_code + self.compute_seq(num_po)
    #         return name
    #     else:
    #         return False

    #t??nh seq cho phi???u mua c??ng vendor
    # def compute_seq(self, num_po):
    #     MAX_LEN = 6
    #     str_num = str(num_po)
    #     l_str = MAX_LEN - len(str_num)
    #     if l_str > 0:
    #         name = ''
    #         for i in range(l_str):
    #             name += '0'
    #         name += str_num
    #     else:
    #         name = False
    #     return name

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    prod_image = fields.Binary(string="???nh s???n ph???m", related="product_id.image_1920")
    declare_ok = fields.Selection([
        ('no', 'Kh??ng (???)'),
        ('yes', 'C?? (???)'),
    ],
        string="KBHQ", default='no')
    qty_available = fields.Float(string="T???n kho", related="product_id.qty_available")
    seq_cus = fields.Integer(string="STT", readonly=True)
    # virtual_available = fields.Float(string="Kh??? d???ng", related="product_tmpl_id.virtual_available")
    # virtual_qty = fields.Char(string="TKKD/ TKTT", compute="purchase_virtual_qty")
    attr_value_ids = fields.Many2many('product.template.attr.value', related="product_id.product_attr_tags",string="Thu???c t??nh")
    attr_value_cn = fields.Char(string = "Gi?? tr???")
    status_order = fields.Selection([
        ('waitting', 'Ch??? ?????t h??ng'),
        ('ordering', '?????t h??ng'),
        ('picking', '?????i s???p chuy???n'),
        ('done', 'T???i B???ng T?????ng'),
    ],
        string="Tr???ng th??i", default='waitting', tracking=True)
    day_to_order = fields.Integer(string="Ng??y ?????t h??ng")
    date_planed = fields.Datetime(string="D??? ki???n")
    update_log = fields.Text(string="L???ch s???")
    note = fields.Text(string="Ghi ch??")
    old_price_unit = fields.Float(string="????n gi??")

    @api.onchange('old_price_unit', 'product_uom_qty')
    def _onchange_price_custom(self):
        self.write({
            'price_unit': self.old_price_unit,
        })

    # @api.onchange('tax_id')
    # def _onchange_price_dis_custom(self):
    #     self.write({
    #         'old_price_unit': self.price_unit,
    #     })

    @api.onchange("product_id")
    def purchase_virtual_qty(self):
        for line in self:
            # virtual_qty = ''
            name = line.product_id.name
            attr_value_cn = ''

            if line.product_id != False:
                # virtual_qty = ("%s/%s") % (line.virtual_available, line.qty_available)
                continue

            if line.attr_value_ids:
                for attr in line.attr_value_ids:
                    attr_value_cn += attr.display_chinese_name +"\n"

            line.update({
                "name": name,
                "attr_value_cn": attr_value_cn,
            })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    prod_image = fields.Binary(string="???nh s???n ph???m", related="product_id.image_1920")
    qty_available = fields.Float(string="T???n kho", related="product_id.qty_available")
    seq_cus = fields.Integer(string="STT", readonly=True)
    # virtual_available = fields.Float(string="Kh??? d???ng", related="product_tmpl_id.virtual_available")
    # virtual_qty = fields.Char(string="TKKD/ TKTT", compute="_virtual_qty")
    attr_value_ids = fields.Many2many('product.template.attr.value', related="product_template_id.product_attr_tags", string="Thu???c t??nh")
    cus_discount = fields.Float(string='C.Kh???u ($)')
    # rename = fields.Boolean(string=False)
    old_price_unit = fields.Float(string='????n gi??', readonly=False)
    low_price = fields.Boolean(default=False)
    note = fields.Char(string='Ghi ch??')

    @api.onchange('old_price_unit', 'product_uom_qty')
    def _onchange_price_custom(self):
        self.write({
            'price_unit': self.old_price_unit,
        })

    @api.onchange('discount', 'tax_id')
    def _onchange_price_dis_custom(self):
        self.write({
            'old_price_unit': self.price_unit,
        })

    # def _compute_amount(self):
    #     vals = {}
    #     for line in self:
    #         if line.change_name:
    #             name = line._new_product_name(line.product_tmpl_id)
    #             vals[line] = {
    #                     "name": name,
    #                     "change_name": False,
    #                 }
    #         for line in vals.keys():
    #             line.update(vals[line])
    #     res = super(SaleOrderLine, self)._compute_amount()
    #     return res

    # @api.onchange('price_unit')
    # def change_price_low(self):
    #     if self._origin.price_unit > self.price_unit:
    #         self.low_price = True
    #     else:
    #         self.low_price = False

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_due = fields.Monetary(string="C??ng n??? hi???n t???i", related="partner_id.total_due")
    state = fields.Selection(selection=[
        ('draft', 'B??o gi??'),
        ('waiting', 'Ch??? duy???t'),
        ('approved', '???? duy???t'),
        ('sent', '???? g???i'),
        ('sale', '????n h??ng'),
        ('done', '???? kh??a'),
        ('return', 'Ho??n ti???n'),
        ('cancel', '???? h???y'),
    ], string='Tr???ng th??i', readonly=True, copy=False,
        index=True, track_visibility='onchange',
        track_sequence=3, default='draft')
    shipping_method = fields.Many2one('delivery.carrier', string="V???n chuy???n", track_visibility='onchange')
    sm_signture = fields.Binary(string="Ch??? k?? NVKD", related="user_id.sign_signature")
    pst_by_word = fields.Char(string="S??? ti???n b???ng ch???", compute='_compute_subtotal_word')
    taxes_ids_all = fields.Many2many("account.tax", string="Thu??? ??p d???ng")
    round_price = fields.Boolean(string="L??m tr??n gi??", default=False)
    change_tax = fields.Boolean(default=False)
    priority = fields.Selection(selection=[
        ('1', 'B??nh th?????ng'),
        ('2', '??u ti??n'),
    ], string='M???c ????? ??u ti??n', default='1', required=True)

    order_quick_ids = fields.One2many("sale.order.quick.line", "order_id", string="D??ng b??o gi?? nhanh")
    quick_subtotal_amount = fields.Monetary(string="T???ng ch??a th???", currency_field='currency_id', compute="_compute_quick_amount")
    quick_tax_amount = fields.Monetary(string="T???ng thu???", currency_field='currency_id', compute="_compute_quick_amount")
    quick_total_amount = fields.Monetary(string="T???ng", currency_field='currency_id', compute="_compute_quick_amount")

    return_order_ids = fields.One2many("return.order.line", "order_id", string="Chi ti???t tr??? l???i")

    all_tax_amount = fields.Monetary(string="T???ng thu???", currency_field='currency_id', compute="_compute_quick_amount")
    all_subtotal_amount = fields.Monetary(string="T???ng ch??a thu???", currency_field='currency_id', compute="_compute_quick_amount")
    all_total_amount = fields.Monetary(string="T???ng", currency_field='currency_id', compute="_compute_quick_amount")

    #tinh b??o gi?? nhanh
    def _compute_quick_amount(self):
        quick_subtotal_amount = 0.0
        quick_tax_amount = 0.0
        quick_total_amount = 0.0

        if self.order_quick_ids:
            for line in self.order_quick_ids:
                if line.is_display:
                    quick_subtotal_amount += line.price_subtotal
                    quick_tax_amount += line.price_tax
                    quick_total_amount += line.price_total

        all_tax_amount = self.amount_tax + quick_tax_amount
        all_subtotal_amount = self.amount_untaxed + quick_subtotal_amount
        all_total_amount = self.amount_total + quick_total_amount
        data = {
            'quick_subtotal_amount': quick_subtotal_amount,
            'quick_tax_amount': quick_tax_amount,
            'quick_total_amount': quick_total_amount,
            'all_tax_amount': all_tax_amount,
            'all_subtotal_amount': all_subtotal_amount,
            'all_total_amount': all_total_amount,
        }
        self.write(data)

    # s??? ti???n b???ng ch???
    @api.depends('all_total_amount', 'amount_total')
    def _compute_subtotal_word(self):
        pst_by_word = ''
        if self.amount_total:
            pst_word = n2w(str(self.all_total_amount / 1000))
            pst_by_word = pst_word.capitalize() + ' ?????ng'
        self.write({
            "pst_by_word": pst_by_word,
        })

    # ?????i t??n s???n ph???m
    # def _new_product_name(self, product_tmpl_id):
    #     name = product_tmpl_id.name
    #     attr_prod = product_tmpl_id.product_template_attribute_value_ids
    #     if attr_prod:
    #         attr_name = ''
    #         for a in attr_prod:
    #             if a.on_print:
    #                 attr_name += a.name + ' '
    #         name = name + ' ( ' + attr_name + ' )'
    #     return name
    #
    # def apply_all_rename(self):
    #     if self.order_line == False:
    #         return False
    #
    #     for line in self.order_line:
    #         if line.rename:
    #             continue
    #
    #         check_name = line.name.find("[", 0, 2)
    #         if check_name != -1:
    #             new_name = self._new_product_name(line.product_tmpl_id)
    #             line.write({
    #                 'name': new_name,
    #                 'rename': True,
    #             })
    #     return True

    # kiem tra chi ph??
    def check_cost_product(self):
        for line in self.order_line:
            if line.purchase_price == 0.0:
                return line.name
        return False

    # ap dung thue, lam tron, stt
    def apply_all_line(self):
        data = {}
        i = 1
        if self.taxes_ids_all and self.change_tax:
            data['tax_id'] = [(6, 0, self.taxes_ids_all.ids)]
            self.write({
                'taxes_ids_all': False,
                'change_tax': False,
            })

        try:
            for line in self.order_line:
                data['seq_cus'] = i
                line.write(data)
                i += 1
        except:
            pass

        try:
            for l in self.order_quick_ids:
                if l.is_display:
                    data['seq_cus'] = i
                    i += 1
                else:
                    data['seq_cus'] = 0
                l.write(data)
        except:
            pass

    @api.onchange("taxes_ids_all")
    def change_taxes_id(self):
        if self._origin.taxes_ids_all != self.taxes_ids_all:
            self.change_tax = True
        else:
            self.change_tax = False

    #xem l???ch s??? b??n h??ng
    def action_view_price_history(self):
        self.ensure_one()
        view_id = self.env.ref('khoakim_customize.view_sale_order_line_history_kk')
        search_view_id = self.env.ref('khoakim_customize.view_sale_order_line_filter_kk')
        result = {
                    "name": "L???ch s??? gi??",
                    "res_model": "sale.order.line",
                    "type": "ir.actions.act_window",
                    "view_mode": "tree",
                    "domain": [('order_partner_id', '=', self.partner_id.id)],
                    "context": {"create": False},
                    "view_id": view_id.ids,
                    "search_view_id": search_view_id.ids,
                }
        return result

    #t???o ho?? ????n
    def customize_sale_confirm(self):
        self.action_confirm()
        return {
            'name': _('Ghi nh???n thanh to??n'),
            'res_model': 'sale.order.invoice.kk',
            'view_mode': 'form',
            'context': {
                'active_model': 'sale.order',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    #kiem tra quyen duyet
    def check_pass_perm(self):
        group_pass = 'khoakim_customize.group_pass_approval_sale_order'
        user_id = self.env.user
        if user_id.has_group(group_pass):
            return True
        return False

    #kiem tra bao gia nhanh
    def check_quick_line(self):
        for line in self.order_quick_ids:
            if line.is_display:
                return True
        return False

    #kiem tra hoan tien va tra lai
    def check_cash_back(self):
        if self.invoice_ids == False:
            return False

        for invoice_id in self.invoice_ids:
            if invoice_id.state == 'posted' and invoice_id.amount_residual < invoice_id.amount_total:
                return True

    #huy don va tra tien
    def cancel_cash_back(self):
        check = self.check_cash_back()
        if check:
            self.write({
                'state': 'return',
            })
        else:
            if self.invoice_ids:
                for invoice_id in self.invoice_ids:
                    invoice_id.button_draft()
            self.action_cancel()

    #xac nhan hoan tien
    

    #kiem tra gia tien bao gia
    # def check_price_quotation(self):
    #     if self.order_line:
    #         for line in self.order_line:
    #             if line.display_type == False :
    #                 return line.name
    #     return False

    #check c?? chiet khau
    # def check_discount(self):
    #     for l in self.order_line:
    #         discount = l.discount or l.cus_discount
    #         if discount > 0.0:
    #             return l.product_tmpl_id.name
    #     return False

    #x??t duy???t b??o gi??
    def action_quotation_approval(self):
        # check_price = self.check_price_quotation()
        # if check_price:
        #     raise UserError(("Vui l??ng ki???m tra l???i s???n ph???m %s ch??a c?? gi?? ti???n") % (check_price))

        # check_perm_pass = self.check_pass_perm()
        check_quick_line = self.check_quick_line()
        # iv = False
        # if self.state in ['draft', 'waiting', 'sent']:
        #     if check_perm_pass == False:
        #         disc = False
        #         if disc:
        #             self.write({'state': 'waiting'})
        #             self.notify_manager()
        #             return {
        #                         'warning': {
        #                                         'title': ('H??y ch??? ch??t'),
        #                                         'message': (("Do s???n ph???m %s ??ang ???????c chi???t kh???u n??n c???n ph???i duy???t! Vui l??ng th??ng b??o t???i kh??ch h??ng") % (disc)),
        #                                     },
        #                     }

        if check_quick_line:
            raise UserError("Vui l??ng ki???m tra v?? b??? t??ch c??c s???n ph???m trong b??o gi?? nhanh")

        return {
            'name': _('Ghi nh???n thanh to??n'),
            'res_model': 'sale.order.invoice.kk',
            'view_mode': 'form',
            'context': {
                'active_model': 'sale.order',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

        # iv = self.customize_sale_confirm()

        # if iv:
        #     return iv.action_register_payment()
        # else:
        #     return {
        #         'warning': {
        #                         'title': ('Ki???m tra l???i c???u h??nh s???n ph???m'),
        #                         'message': ("Kh??ng th??? t???o h??a ????n theo ????n h??ng"),
        #                     },
        #     }

    #x??c nh???n b??o gi??
    def action_accept_approval(self):
        # iv = self.customize_sale_confirm()
        # if iv:
        #     return iv.action_register_payment()
        # else:
        #     return {
        #         'warning': {
        #                         'title': ('Ki???m tra l???i c???u h??nh s???n ph???m'),
        #                         'message': ("Kh??ng th??? t???o h??a ????n theo ????n h??ng"),
        #                     },
        #     }
        self.write({'state': 'approved'})
        self.notify_manager()

    def action_deny_approval(self):
        self.write({'state': 'draft'})

    def notify_manager(self):
        if self.state == 'waiting':
            manager = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).parent_id
            if manager:
                for sale_approval in self.filtered(lambda hol: hol.state == 'waiting'):
                    # print(sale_approval)
                    sale_approval.activity_schedule(
                        'khoakim_customize.mail_act_sale_approval_kk',
                        user_id=manager.user_id.id or self.env.uid)
            else:
                return {
                        'warning': {
                            'title': ('???? c?? l???i'),
                            'message': (("Ch??a t??m ???????c ng?????i duy???t, vui l??ng li??n h??? admin!")),
                        },
                    }

        self.filtered(lambda hol: hol.state in ['sale', 'approved', 'done']).activity_feedback(
            ['khoakim_customize.mail_act_sale_approval_kk'])
        self.filtered(lambda hol: hol.state in ['draft', 'cancel']).activity_unlink(
            ['khoakim_customize.mail_act_sale_approval_kk'])
        if self.state == 'draft':
            for sale_deny in self.filtered(lambda hol: hol.state == 'draft'):
                sale_deny.activity_schedule(
                    'khoakim_customize.mail_act_sale_approval_kk',
                    user_id = sale_deny.user_id.id or self.env.uid)

    @api.model
    def create(self, vals):
        rec = super(SaleOrder, self).create(vals)
        self.apply_all_line()
        return rec

    def write(self, vals):
        rec = super(SaleOrder, self).write(vals)
        self.apply_all_line()
        # self.apply_all_rename()
        return rec

class ResCompanyAccountLine(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'res.company.account.lines'
    _rec_name = 'name'
    _description = 'Th??ng tin t??i kho???n'

    company_id = fields.Many2one('res.company', string='C??ng ty')
    name = fields.Char(string='T??i kho???n', compute='_compute_name')
    type = fields.Selection([
                                ('person', 'C?? nh??n'),
                                ('company', 'C??ng ty'),
                            ], string='Lo???i t??i kho???n', default='person', require=True)
    acc_holder = fields.Char(string='T??n t??i kho???n', require=True)
    acc_number = fields.Char(string='S??? t??i kho???n', require=True)
    bank_id = fields.Many2one('res.bank', string="Ng??n h??ng", require=True)
    branch = fields.Char(string='Chi nh??nh')
    qr_code = fields.Binary(string='M?? QR code')

    @api.depends('acc_number', 'bank_id.name')
    def _compute_name(self):
        for line in self:
            if line.bank_id.name and line.acc_number:
                line.name = line.acc_number + ' - ' + line.bank_id.name
            else:
                line.name = ''

class ResCompany(models.Model):
    _inherit = 'res.company'

    wp_url = fields.Char(string='Link website')
    wp_user = fields.Char(string='T??i kho???n WP')
    wp_pass = fields.Char(string='M???t kh???u WP')
    woo_ck = fields.Char(string='Keys Woocommerce')
    woo_cs = fields.Char(string='Secret Woocommerce')
    sign_company = fields.Binary(string='D???u c??ng ty')
    account_lines = fields.One2many('res.company.account.lines', 'company_id',
                                    string='T??i kho???n ng??n h??ng')
    purc_amount = fields.Float(string="T??? l??? gi?? v???n", default=100.0)
    purc_comp_id = fields.Many2one('res.company', string="C??ng ty mua h??ng m???c ?????nh", required=True)
    check_std_price = fields.Boolean(default=False)

    @api.onchange('purc_amount', 'purc_comp_id')
    def _onchange_check_std_price(self):
        if self.check_std_price and self.purc_amount != 100.0:
            self.write({
                'check_std_price': False,
            })

    def action_check_std_price(self):
        if self.check_std_price == False:
            return {
                'name': _('C???p nh???t gi?? v???n'),
                'res_model': 'std.price.change',
                'view_mode': 'form',
                'context': {
                    'active_model': 'res.company',
                    'active_ids': self.ids,
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_amount = fields.Float(string="T???ng ti???n", compute="compute_total_amount")
    priority_so = fields.Selection(selection=[
        ('1', 'B??nh th?????ng'),
        ('2', '??u ti??n'),
    ], string='M??c ????? ??u ti??n', default='1')

    @api.depends('move_line_ids_without_package')
    def compute_total_amount(self):
        for picking in self:
            total_amount = 0
            if picking.sale_id:
                for line in picking.move_line_ids_without_package:
                    total_amount += line.total_amount
            picking.total_amount = total_amount

    def action_check_out_wh(self):
        if self.picking_type_code == 'outgoing':
            if self.move_ids_without_package:
                for line in self.move_ids_without_package:
                    prod = line.product_tmpl_id
                    if (prod.weight == False or prod.volumn == False ):
                        raise UserError(("Vui l??ng ki???m tra l???i s???n ph???m %s ch??a c?? kh???i l?????ng ho???c th??? t??ch") % (prod.name))
        self.action_confirm()

    # def _create_return_line(self):
    #     return_type = self.picking_id.picking_type_id.return_picking_type_id.id or self.picking_id.picking_type_id.id
    #

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    prod_image = fields.Binary(string="???nh s???n ph???m", related="product_id.image_1920")
    price_unit = fields.Float(string="????n gi??", compute="_computed_lst_price")
    price_tax = fields.Float(string="T??ng thu???", compute="_computed_lst_price")
    total_amount = fields.Float(string="Th??nh ti???n", compute="_computed_lst_price")
    purchase_price = fields.Float(string="Chi ph??", compute="_computed_lst_price")
    seq_cus = fields.Integer(string="STT", readonly=True)
    attr_value_ids = fields.Many2many('product.template.attr.value', related="product_id.product_attr_tags",string="Thu???c t??nh")

    def _computed_lst_price(self):
        for line in self:
            sale_id = line.picking_id.sale_id
            price_unit = 0
            price_tax = 0
            total_amount = 0
            purchase_price = 0
            if sale_id:
                product_tmpl_id = self.product_id.product_tmpl_id
                price_unit = product_tmpl_id.price_unit
                purchase_price = product_tmpl_id.purchase_price
                if product_tmpl_id.product_uom_qty:
                    price_tax = (float(product_tmpl_id.price_tax) / float(product_tmpl_id.product_uom_qty)) * line.qty_done
                total_amount = price_tax + (float(product_tmpl_id.price_unit) * line.qty_done)
            line.write({
                            'price_unit': price_unit,
                            'price_tax': price_tax,
                            'total_amount': total_amount,
                            'purchase_price': purchase_price,
                        })

class StockMove(models.Model):
    _inherit = 'stock.move'

    prod_image = fields.Binary(string="???nh s???n ph???m", related="product_tmpl_id.image_1920")
    attr_value_ids = fields.Many2many('product.template.attr.value', related="product_id.product_attr_tags",
                                      string="Thu???c t??nh")

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    total_weight = fields.Float(string='T???ng tr???ng l?????ng', compute="total_weight_prod")
    total_volume = fields.Float(string='T???ng kh???i l?????ng')

    @api.depends('picking_ids')
    def total_weight_prod(self):
        total_weight = 0
        if self.picking_ids:
            for picking_id in self.picking_ids:
                total_weight += picking_id.weight
        self.total_weight = total_weight
        if self.cost_lines:
            for line in self.cost_lines:
                if line.provisional == True:
                    line.provisional = False

class StockLandedCostLines(models.Model):
    _inherit = 'stock.landed.cost.lines'

    total_weight = fields.Float(related="cost_id.total_weight")
    provisional = fields.Boolean(string="T???m t??nh")

    @api.onchange('provisional', 'total_weight', 'split_method')
    def total_weight_compute(self):
        if self.provisional and self.split_method == 'by_weight':
            total_price = self.product_tmpl_id.standard_price * self.total_weight
            self.price_unit = total_price

class ReturnOrderLine(models.Model):
    _name = 'return.order.line'
    _description = '????n tr??? h??ng'

    order_id = fields.Many2one('sale.order', required=True, ondelete="cascade")
    picking_id = fields.Many2one('stock.picking', required=True, ondelete="cascade")
    date_done = fields.Datetime(string='Ng??y th???c hi???n', required=True)
    # product_tmpl_id = fields.Many2one('product.product', string="S???n ph???m")
    product_tmpl_id = fields.Many2one('product.template', string="S???n ph???m")
    product_uom = fields.Many2one('uom.uom', string='????n v???', related="product_tmpl_id.uom_id")
    product_qty = fields.Float(string='S??? l????ng', default=1.0)
    price_unit = fields.Float(string="????n gi??", compute="_compute_price_total")
    price_tax = fields.Float(string="T???ng thu???", compute="_compute_price_total")
    total_amount = fields.Float(string="T???ng ti???n", compute="_compute_price_total")
    done_return = fields.Boolean(string='Ch???p nh???n ho??n')
    partner_id = fields.Many2one('res.partner', string='Kh??ch h??ng', related="order_id.partner_id")
    purchase_price = fields.Float(string="Chi ph??", compute="_compute_price_total")
    picking_state = fields.Char(string='Tr???ng th??i')

    # @api.depends("picking_state")
    # def _compute_return(self):
    #     for rec in self:
    #         if rec.state == 'done':
    #             rec.done_return = True
    #         else:
    #             rec.done_return = False

    @api.depends('order_id', 'product_tmpl_id', 'product_qty')
    def _compute_price_total(self):
        sale_order = self.env['sale.order.line']
        for line in self:
            so_line = sale_order.search([('order_id', '=', line.order_id.id),
                                         ('product_tmpl_id', '=', line.product_tmpl_id.id)], limit=1)
            if so_line:
                price_tax = (float(so_line.price_tax) / float(so_line.product_uom_qty)) * line.product_qty
                total_amount = float(so_line.price_unit) * float(line.product_qty) + price_tax
                data = {
                    'price_unit': so_line.price_unit,
                    'purchase_price': so_line.purchase_price,
                    'price_tax': price_tax,
                    'total_amount': total_amount,
                }
                line.update(data)

class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        # Prevent copy of the carrier and carrier price when generating return picking
        # (we have no integration of returns for now)
        new_picking, pick_type_id = super(StockReturnPicking, self)._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        if picking.group_id.sale_id:
            order_id = picking.group_id.sale_id
            data = {
                        "order_id": order_id.id,
                        "picking_id": picking.id,
                        "date_done": fields.Datetime.now(),
                    }
            for line in picking.move_ids_without_package:
                data["product_tmpl_id"] = line.product_tmpl_id.id
                data["product_qty"] = line.product_uom_qty
            self.env["return.order.line"].create(data)
        return new_picking, pick_type_id

class QuickSaleOrderLine(models.Model):
    _name = 'sale.order.quick.line'
    _description = 'B??o gi?? nhanh'

    order_id = fields.Many2one('sale.order', required=True, ondelete="cascade")
    so_line_id = fields.Integer(sting="D??ng b??o gi??")
    # product_tmpl_id = fields.Many2one('product.product', string="S???n ph???m")
    product_tmpl_id = fields.Many2one('product.template', string="S???n ph???m")
    catg_prod_id = fields.Many2one('product.category', string="Danh m???c")
    prod_code = fields.Char(string='M?? s???n ph???m')
    seq_cus = fields.Integer(string="STT", readonly=True)
    # catg_prod = fields.Many2one()
    prod_image = fields.Binary(string="???nh s???n ph???m")
    attrs_prod_1 = fields.Char(string="Thu???c t??nh 1")
    attrs_prod_2 = fields.Char(string="Thu???c t??nh 2")
    attrs_prod_3 = fields.Char(string="Thu???c t??nh 3")
    name = fields.Char(string='T??n s???n ph???m', required=True)
    product_qty = fields.Float(string='S??? l????ng', default=1.0)
    # product_uom = fields.Char(string="????n v???", default="C??i")
    product_uom = fields.Many2one('uom.uom', '????n v???', required=True)
    price_unit = fields.Float(string="????n gi??")
    tax_id = fields.Many2many('account.tax', string='Thu???', context={'active_test': False})
    partner_id = fields.Many2one('res.partner', string='Kh??ch h??ng')
    price_tax = fields.Float(string='T???ng thu???', compute='_compute_price_tax_kk')
    price_subtotal = fields.Float(string='T???ng ch??a thu???', compute='_compute_price_tax_kk')
    price_total = fields.Float(string='T???ng', compute='_compute_total_kk')
    vendor_id = fields.Many2one('res.partner', string='Nh?? cung c???p')
    note = fields.Text(string="Ghi ch??")
    company_id = fields.Many2one('res.company', string='C??ng ty')
    purchase_price = fields.Float(string='Chi ph??')
    is_display = fields.Boolean(string='BG', default=True)
    code_product = fields.Char(string="M?? s???n ph???m")
    so_state = fields.Selection(selection=[
                                                ('draft', 'B??o gi??'),
                                                ('waiting', 'Ch??? duy???t'),
                                                ('approved', '???? duy???t'),
                                                ('sent', '???? g???i'),
                                                ('sale', '????n h??ng'),
                                                ('done', '???? kh??a'),
                                                ('cancel', '???? h???y'),
                                            ], string='Tr???ng th??i', readonly=True,
                                                copy=False, related="order_id.state")

    @api.depends("tax_id", "price_unit", "product_qty")
    def _compute_price_tax_kk(self):
        for line in self:
            price_tax = 0
            price_subtotal = line.price_unit * line.product_qty
            for tax in line.tax_id:
                amount = 0
                disc = 0
                if tax.amount_type == "fixed":
                    amount = tax.amount
                if tax.amount_type == "percent":
                    disc = tax.amount
                price_tax += amount + disc * price_subtotal/100
            line.write({
                'price_tax': price_tax,
                'price_subtotal': price_subtotal,
            })

    @api.depends("price_subtotal", "price_tax")
    def _compute_total_kk(self):
        for line in self:
            price_total = line.price_subtotal + line.price_tax
            line.write({
                'price_total': price_total,
            })

    @api.onchange("purchase_price")
    def _default_price_unit(self):
        if self.price_unit == 0:
            self.price_unit = self.purchase_price * 1.5

    def button_add_product(self):
        return {
            'name': _('T???o s???n ph???m nhanh'),
            'res_model': 'product.product.create',
            'view_mode': 'form',
            'context': {
                'active_model': 'sale.order.quick.line',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

#Thu???c t??nh v?? gi?? tr???
class ProductTemplateAttributeValue(models.Model):
    _name = 'product.template.attr.value'
    _description = 'Gi?? tr??? thu???c t??nh s???n ph???m'
    _rec_name = 'display_name'

    name = fields.Char(string="Gi?? tr??? thu???c t??nh", required=True)
    display_name = fields.Char(string="Gi?? tr??? thu???c t??nh",
                               compute="_compute_display_name")
    chinese_name = fields.Char(string="Ti???ng Trung")
    display_chinese_name = fields.Char(string="Gi?? tr??? thu???c t??nh",
                                       compute="_compute_display_name")
    color = fields.Integer(string="color")
    acode = fields.Char(string="M?? bi???n th???", required=True)
    sequence = fields.Integer(string="Quy t???c m??")
    attr_id = fields.Many2one('product.template.attr',
                                    string="Thu???c t??nh")

    @api.depends('attr_id', 'name', 'chinese_name')
    def _compute_display_name(self):
        for rec in self:
            display_name = ''
            display_chinese_name = ''

            if rec.attr_id:
                if rec.name:
                    display_name = rec.attr_id.name + " : " + rec.name
                if rec.chinese_name:
                    display_chinese_name = rec.attr_id.chinese_name + " : " + rec.chinese_name

            rec.display_name = display_name
            rec.display_chinese_name = display_chinese_name

class ProductTemplateAttribute(models.Model):
    _name = 'product.template.attr'
    _description = 'Thu???c t??nh s???n ph???m'

    name = fields.Char(string="Thu???c t??nh", required=True)
    sequence = fields.Integer(string="Quy t???c m??")
    chinese_name = fields.Char(string="T??n Trung qu???c", required=True)
    on_print = fields.Boolean(string="Hi???n tr??n b???n in", default=True)
    product_tmpl_ids = fields.Many2many("product.template",string="S???n ph???m li??n quan")
    attr_value_ids = fields.One2many('product.template.attr.value', 'attr_id',
                                         string="Gi?? tr??? thu???c t??nh")
    # count_values = fields.Integer(string="S??? l?????ng gi?? tr???", compute="_compute_count")
    # count_prod = fields.Integer(string="S??? l?????ng s???n ph???m", compute="_compute_count")
    #
    # @api.depends("value_ids", "count_prod")
    # def _compute_count(self):
    #     count_prod = 0
    #     count_values = 0
    #     self.write({
    #         "count_prod": count_prod,
    #         "count_values": count_values,
    #     })
    #     return True

# Module t??nh gi??

# class BrandProductPrice(models.Model):
#     _name = 'price.brand.product'
#     _description = 'Nh??n hi???u'
#
#     name = fields.Char(string='T??n h??ng', required=True)
#     code = fields.Char(string='M?? h??ng', required=True)
#
# class ProductSeries(models.Model):
#     _name = 'series.product'
#     _description = 'D??ng s???n ph???m'
#
#     series_image = fields.Binary(string="???nh d??ng s???n ph???m")
#     name = fields.Char(string='T??n d??ng s???n ph???m', required=True)
#     code = fields.Char(string='M?? d??ng', required=True)
#     parent_sp = fields.Many2one('series.product', string="D??ng s???n ph???m cha")
#     is_display = fields.Boolean(default=False)
#
# class ProductPriceList(models.Model):
#     _name = 'pricelist.product'
#     _description = 'B???ng gi?? s???n ph???m'
#
#     name = fields.Char(string="T??n b???ng gi??", required=True)
#     brand = fields.Many2many('price.brand.product', string="H??ng")
#     is_rule = fields.Boolean(string="C?? quy t???c", default=False)
#     vendor_id = fields.Many2one('res.partner', string="Nh?? cung c???p")

# class WPSetting(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     wp_url = fields.Char(string='URL website')
#     wp_user = fields.Char(string='T??i kho???n WP')
#     wp_pass = fields.Char(string='M???t kh???u WP')
#     woo_ck = fields.Char(string='Keys Woocommerce')
#     woo_cs = fields.Char(string='Secret Woocommerce')