from odoo import models,_,api,fields


class Partner(models.Model):

    _inherit = 'res.partner'

    lead_id = fields.One2many('crm.lead', 'partner_id')