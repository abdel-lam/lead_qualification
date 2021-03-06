{
    'name': 'Lead Qualification',
    'author': 'lamrabti abdellatif',
    'summary': '',
    'description': "",
    'website': "https://github.com/abdel-lam/lead_qualification",
    'depends': ['crm','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_activity_data.xml',
        'report/report.xml',
        'report/report_template.xml',
        'wizard/customer_lead_wizard.xml',
        'views/crm_lead_views.xml',
        'views/res_partner_views.xml',
        'views/portal_crm_lead_deadline_template.xml',


    ],
    'assets': {
        'web.assets_backend': [
            'lead_qualification/static/src/js/lead_activity.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}