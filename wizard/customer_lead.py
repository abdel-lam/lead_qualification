from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class CustomerLead(models.TransientModel):
    _name = 'customer.lead'
    _description = 'create lead from customer form'

    lead_states = fields.Selection([('new', 'Nouveau'),
                                ('created', 'Créer')],
                                string='Status', tracking=True, default='new')
    name = fields.Char('Client')
    piste = fields.Char('Piste')

