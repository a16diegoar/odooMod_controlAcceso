# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class WizardAskUser(models.TransientModel):
	_name = 'acceso.wizard_acceso'
	_description = "Wizard: Selección de usuario"

	usuario_id = fields.Many2one('res.partner', string="Usuario", required=True)
	sala_id = fields.Many2one('acceso.sala', string="Sala", required=True)
