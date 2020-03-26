# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Sala(models.Model):
	_name = 'acceso.sala'
	_description = 'Sala'

	name = fields.Char('Nombre')
	number = fields.Integer('Numero')
	descr = fields.Text("Descipción")

	accesos_ids = fields.Many2many('acceso.regla', string="Accesos")


class ResGroups(models.Model):
	_inherit = 'res.groups'

	nusuarios = fields.Integer(
		string="Numero de usuarios",
		compute="_compute_nusuarios",
		store=False,
		compute_sudo=False
	)

	@api.depends('users')
	def _compute_nusuarios(self):
		sql = "select uid from res_groups_users_rel where gid = %s"
		params = (self.id,)
		self.env.cr.execute(sql, params)
		result = self.env.cr.fetchall()

		self.nusuarios = len(result)

		_logger.info("BUUDEBUUUG")
		_logger.info(result)


class Regla(models.Model):
	_name = 'acceso.regla'

	name = fields.Char("Regla")
	description = fields.Text("Descripcion")

	salas = fields.Many2many('acceso.sala')
	