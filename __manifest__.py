# -*- coding: utf-8 -*-

{
    'name': 'Website Academy',
    'version': '1.0',
    'summary': '',
    'description': """
    """,
    'website': '',
    'author': '',
    'depends': [
        'contacts', 'website'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'wizard/report_wizard.xml',
        'report/course_summary.xml',
    ],
    'sequence': 1,
    'installable': True,
}
