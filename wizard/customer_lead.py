from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class CustomerLead(models.TransientModel):
    _name = 'customer.lead'
    _description = 'create lead from customer form'

    lead_states = fields.Selection([('new', 'Nouveau'),
                                ('creat', 'Créer')],
                                string='Status', tracking=True, default='new')
    name = fields.Many2one('res.partner','Client')
    piste = fields.Char('Piste')

    def action_next(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Change Customer Field',
                'res_model': 'customer.lead',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_name': rec.name.id,
                    'default_lead_states': 'creat',
                }
            }

    def create_lead(self):
        vals = {
            "name": self.piste,
            "partner_id": self.name.id,
            "user_id": None,
        }
        return self.env["crm.lead"].create(vals)


