# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _get_default_satges(self):
        stages = self.env['project.task.type'].search([('default_stage', '=', True)])
        return stages

    type_ids = fields.Many2many('project.task.type', 'project_task_type_rel', 
        'project_id', 'type_id', string='Tasks Stages', default=_get_default_satges)


    @api.model
    def create(self, vals):
        if vals.get('type_ids'):
            stages = self.env['project.task.type'].search([('default_stage', '=', True)])
            for stage in stages:
                if stage.id in self.type_ids.ids and stage.id not in vals.get('type_ids')[0][2]:
                    raise ValidationError(_('Error ! You cannot Delete default stage.'))
        return super(ProjectProject, self).create(vals)

    def write(self, vals):
        if vals.get('type_ids'):
            stages = self.env['project.task.type'].search([('default_stage', '=', True)])
            for stage in stages:
                if stage.id in self.type_ids.ids and stage.id not in vals.get('type_ids')[0][2]:
                    raise ValidationError(_('Error ! You cannot Delete default stage.'))
        return super(ProjectProject, self).write(vals)



class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    default_stage = fields.Boolean(string='Default for New Projects',
        help='If you check this field, this stage will by default '
             'on each new project. It will not assign this stage to existing '
             'projects.')

    def unlink(self):
        for rec in self:
            if rec.default_stage:
                raise UserError(_('You cannot delete Default stages.'))
        return super(ProjectTaskType, self).unlink()
