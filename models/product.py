# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.website.models.website import slug

class PolicyType(models.Model):
    """docstring for Policy Holder Type"""
    _name =  'ng_insurance_retail.policy.type'

    name =  fields.Char(string='Name')
    description =  fields.Text(string='Description')
    features =  fields.Html(string='Features')


class Product(models.Model):
    """The insurance service or product being purchased by the customer a.k.a (policy holder)"""

    _inherit = 'product.template'

    policy = fields.Boolean(string='Policy')
    type_id = fields.Many2one('ng_insurance_retail.policy.type', string='Policy Type')
    premium_type = fields.Selection(selection=[('fixed', 'Fixed'),('rated', 'Rated')], string='Premium Type')
    policy_period = fields.Float(string='Policy Period(Years)', defualt=1)
    list_price = fields.Float(string='Premium')
    slug = fields.Char(string='Slug', compute='_compute_slug')

    @api.one
    def _compute_slug(self):
        self.slug =  slug(self)
