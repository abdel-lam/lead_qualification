from odoo import models,_,api,fields


class Lead(models.Model):

    _inherit = 'crm.lead'

    close_date = fields.Date('Close date')