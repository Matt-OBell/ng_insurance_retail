# -*- coding: utf-8 -*-
from odoo import http
from ast import literal_eval
import werkzeug
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
import random
from odoo.fields import Datetime
from datetime import timedelta, datetime

view = http.request

class InsuranceWebsiteSale(WebsiteSale):
    """WebsiteSale."""

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        """End of checkout process controller. Confirmation is basically seing.
        the status of a sale.order. State at this point :
         - should not have any context / session info: clean them
         - take a sale.order id, because we request a sale.order and are not
           session dependant anymore
        """
        sale_order_id = view.session.get('sale_last_order_id')
        partner_id =  view.env.user.partner_id
        if sale_order_id:
            sale_order_id = view.env['sale.order'].sudo().browse(int(sale_order_id))
            lines = sale_order_id.order_line
            policy_line = view.env['policies.holder.line']
            for line in lines:
                code = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
                policy_line.sudo().create({'name':lines.product_id.id, 
                    'premium':lines.price_unit, 
                    'policy_code':code, 
                    'line_id':partner_id.id,
                    'start_date':Datetime.now(), 'end_date':Datetime.to_string(timedelta(days=lines.product_id.policy_period*360)+ datetime.now())})
            s = super(InsuranceWebsiteSale, self).payment_confirmation()
            view.session['sale_last_order_id'] = False
            return s
        return 

class Website(Website):
    """docstring for Website"""
    @http.route('/', auth='public', website=True)
    def index(self, **kw):
        policies =  view.env['product.product'].sudo().search([('policy', '=', True)])
        qcontext = {'policies': policies}
        return view.render('ng_insurance_retail.policies', qcontext)
  

class NgInsuranceRetail(http.Controller):
    """."""

    @http.route('/subscriber/new/', auth='public', website=True)
    def new(self, **kw):
        return view.render('ng_insurance_retail.index_page')

    @http.route('/subscriber/store/', auth='public', website=True, method=['POST'])
    def store(self, **kw):
        params = [
            'first_name', 'last_name', 'title', 'marital_status', 
            'Agent', 'sex', 'phone', 'address','religion','lga',
            'policy_holder_type','email','occupation'
        ]
        total =  len(params)
        values = {param:kw.get(param) for param in params if kw.get(param)}
        if total != len(values):
            # die minute validation
            error = 'some required field are missing'
            # print '***************', error, values
            return werkzeug.utils.redirect('/subscriber/new', 303)
        config_param = view.env['ir.config_parameter']
        template_user_id = literal_eval(config_param.sudo().get_param('auth_signup.template_user_id', 'False'))
        template_user = view.env['res.users'].sudo().browse(template_user_id)
        name =  '{} {}'.format(values.get('first_name'), values.get('last_name'))
        # title =  view.env['res.partner.title'].name_search(name=values.get('title'))
        res_partner =  view.env['res.partner'].sudo().create({
            'name' : name,
            # 'title' :  False,
            'occupation': values.get('occupation'),
            'religion': values.get('religion'),
            'phone': values.get('phone'),
            'mobile': values.get('phone'),
            'email': values.get('email'),
            'sex':values.get('sex'),
            'street':values.get('address'),
            'is_policy_holder' : True,
            'active' : True,
            })
        if res_partner and template_user:
            user_id = template_user.with_context(no_reset_password=False).sudo().copy({
                'login':res_partner.email, 
                'name': res_partner.name,
                'partner_id': res_partner.id,
                'active': True
            })
            crm = view.env['crm.lead'].sudo().create({'name':user_id.name, 'email_from':user_id.login, 'partner_id':user_id.partner_id.id,
                'phone':user_id.phone or user_id.partner_id.phone})
            print crm
            return werkzeug.utils.redirect('/subscriber/confirmation', 303)

    @http.route('/subscriber/confirmation/', auth='public', website=True)
    def confirmation(self, **kw):
        return view.render('ng_insurance_retail.confirmation')

    @http.route('/ng_insurance_retail/ng_insurance_retail/objects/<model("ng_insurance_retail.ng_insurance_retail"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('ng_insurance_retail.object', {
            'object': obj
        })