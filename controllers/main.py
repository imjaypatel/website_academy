# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class Courses(http.Controller):
    @http.route(['/courses'], type='http', auth="public", website=True)
    def courses(self, **kw):
        courses = request.env['res.courses'].search([])
        values = {
            'courses': courses
        }
        return request.render("website_academy.courses", values)

    @http.route(['/course/<model("res.courses"):course>'], type='http', auth="public", website=True)
    def course(self, course, **kw):
        values = {'course': course}
        return request.render("website_academy.course", values)
