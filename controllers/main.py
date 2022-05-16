# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import werkzeug.urls

from collections import OrderedDict
from werkzeug.exceptions import NotFound

from odoo import fields
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_partner.controllers.main import WebsitePartnerPage

from odoo.tools.translate import _


class WebsiteAccount(CustomerPortal):

    def get_domain_my_lead_custom(self, user):
        return [
            #('partner_assigned_id', 'child_of', user.commercial_partner_id.id),
            ('type', '=', 'lead'),
            ('activity_state', '=', 'overdue'),
        ]



    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'lead_count' in counters:
            values['lead_count'] = request.env['crm.lead'].search_count(self.get_domain_my_lead_custom(request.env.user))
        return values

    @http.route(['/my/leads', '/my/leads/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_leads(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['crm.lead']
        domain = self.get_domain_my_lead_custom(request.env.user)

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'contact_name': {'label': _('Contact Name'), 'order': 'contact_name'},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # pager
        lead_count = CrmLead.search_count(domain)
        pager = request.website.pager(
            url="/my/leads",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=lead_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        leads = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'leads': leads,
            'page_name': 'lead',
            'default_url': '/my/leads',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("lead_qualification.portal_my_leads_custom", values)

    @http.route(['''/my/lead/<model('crm.lead', "[('type','=', 'lead')]"):lead>'''], type='http', auth="user",
                website=True)
    def portal_my_lead(self, lead, **kw):
        if lead.type != 'lead':
            raise NotFound()
        return request.render("lead_qualification.portal_my_lead_custom", {'lead': lead})