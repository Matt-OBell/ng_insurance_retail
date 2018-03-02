# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LGA(models.Model):
    _name = 'res.lga'

    name =  fields.Char(string='Name')        


class Partner(models.Model):
    """The purchaser of an insurance policy. Also called Customers or Subscribers"""

    _inherit = 'res.partner'

    is_policy_holder = fields.Boolean(string='Policy Holder')
    is_agent = fields.Boolean(string='Agent')
    agent_id = fields.Many2one('res.users', string='Agent')
    lga =  fields.Many2one('res.lga', string='LGA')
    occupation = fields.Char(string='Occupation')
    religion =  fields.Char(string='Religion')
    sex  =  fields.Char(string='Sex')
    policy_ids =  fields.One2many('policies.holder.line', 'line_id', string='Policies')
    unique = fields.Char(string='Registration', compute='_compute_unque_code', strore=True)


    @api.depends('is_policy_holder', 'is_agent')
    def _compute_unque_code(self):
        pass

class PoliciesHolderLine(models.Model):
    """docstring for PoliciesHolderLine"""

    _name = 'policies.holder.line'

    name =  fields.Many2one('product.product', string='Policies')
    policy_code = fields.Char(string='Policy Code')
    premium = fields.Float(string='premium')
    line_id = fields.Many2one('res.partner')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='Start Date')
        
