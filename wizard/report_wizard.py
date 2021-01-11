# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CourseSummaryReportWizard(models.TransientModel):
    _name = 'course.summary.report.wizard'

    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('website_academy.course_summary_report').report_action(
            self, data=data)
