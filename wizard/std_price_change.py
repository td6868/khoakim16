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

class StdPriceChange(models.TransientModel):
    _name = "std.price.change"

    def get_infor_company(self):
        id = self.env.context.get('active_ids')
        com_id = self.env['res.company'].browse(id)
        purc_amount = com_id.purc_amount
        purc_comp_id = com_id.purc_comp_id
        return purc_amount, purc_comp_id

    def change_std_price(self):
        purc_amount, purc_comp_id = self.get_infor_company()
        product = self.evn['product.product']
        all_product = product.search([('company_id','=',purc_comp_id.id),('standard_price','>', 0.0)])
        for prod_id in all_product:
            print(prod_id.standard_price)