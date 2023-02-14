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
        ir_property = self.env['ir.property']
        product_model = self.env['ir.model'].search([('model', '=', 'product.template')])
        std_prc_field = self.env['ir.model.fields'].search([('model_id', '=', product_model.id),
                                                            ('name', '=', 'standard_price')])
        all_product = ir_property.search([('company_id', '=', purc_comp_id.id),
                                          ('fields_id', '=', std_prc_field.id)])

        for prod_id in all_product:
            try:
                ir_property.create(
                    {
                        'name': 'standard_price',
                        'company_id': self.env.company.id,
                        'fields_id': std_prc_field.id,
                        'type': 'float',
                        'res_id': prod_id.res_id,
                        'value_float': (prod_id.value_float * purc_amount)/100,
                    }
                )
            except:
                ir_property.update({
                    'value_float': (prod_id.value_float * purc_amount) / 100
                })