# -*- coding: utf-8 -*-

import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.translate import html_translate


class Lessons(models.Model):
    _name = 'res.lessons'
    _description = "Resource Lessons"

    name = fields.Char(string="Lesson Name", required=True)


class Rooms(models.Model):
    _name = 'res.rooms'
    _description = "Resource Rooms"

    name = fields.Char(string="Room Name", required=True)
    capacity = fields.Integer(string="Room Capacity", default=20, required=True)
    lesson_id = fields.Many2one(
        'res.lessons', string="Lesson", required=True, ondelete='cascade')


class Attendees(models.Model):
    _name = 'res.attendees'
    _description = "Resource Attendees"

    name = fields.Char(string="Attendee Name", required=True)
    course_id = fields.Many2one(
        'res.courses', string="Course", ondelete='cascade')


class Courses(models.Model):
    _name = 'res.courses'
    _description = "Resource Courses"

    @api.model
    def _tz_get(self):
        return [(x, x) for x in pytz.all_timezones]

    name = fields.Char(string="Course Name", required=True)
    description = fields.Html(
        'Course Description', sanitize_attributes=False, translate=html_translate)
    instructor_id = fields.Many2one(
        'res.partner', string="Instructor", required=True, ondelete='cascade')
    room_id = fields.Many2one(
        'res.rooms', string="Room", required=True, ondelete='cascade')
    attendees_ids = fields.One2many('res.attendees', 'course_id', string="Attendees")
    lesson_id = fields.Many2one(
        'res.lessons', related='room_id.lesson_id', string='Lesson',
        readonly=True, store=False)
    address_id = fields.Many2one(
        'res.partner', string='Location',
        default=lambda self: self.env.company.partner_id, readonly=False)
    date_begin = fields.Datetime(string='Start Date', required=True)
    date_end = fields.Datetime(string='End Date', required=True)
    date_tz = fields.Selection(
        '_tz_get', string='Timezone',
        required=True, default=lambda self: self.env.user.tz or 'UTC')

    @api.model
    def create(self, vals):
        if 'attendees_ids' in vals and 'room_id' in vals:
            room_id = vals.get('room_id')
            room = self.env['res.rooms'].browse(room_id)

            if len(vals.get('attendees_ids')) > room.capacity:
                raise UserError(_('Attendees can not exceed from the room capacity. Room capacity are only %s people.' % (room.capacity)))

        return super(Courses, self).create(vals)

    def write(self, vals):
        if 'attendees_ids' in vals:
            if 'room_id' in vals:
                room_id = vals.get('room_id')
                room = self.env['res.rooms'].browse(room_id)
            else:
                room = self.room_id

            if len(vals.get('attendees_ids')) > room.capacity:
                raise UserError(_('Attendees can not exceed from the room capacity. Room capacity are only %s people.' % (room.capacity)))

        return super(Courses, self).write(vals)

    @api.onchange('instructor_id')
    def _onchange_instructor_id(self):
        if self.instructor_id:
            course = self.search([('instructor_id', '=',  self.instructor_id.id)])
            if course:
                raise UserError(_('Instructor already assigned in another course.'))

    @api.onchange('room_id')
    def _onchange_room_id(self):
        if self.room_id:
            course = self.search([('room_id', '=',  self.room_id.id)])
            if course:
                raise UserError(_('Room already assigned in another course.'))


class Instructor(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean("Instructor", default=False)
    courses_ids = fields.Many2many('res.courses', string="Courses")
