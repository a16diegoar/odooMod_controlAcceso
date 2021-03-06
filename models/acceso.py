# -*- coding: utf-8 -*-

import logging
import datetime
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Sala(models.Model):
	_name = 'acceso.sala'
	_description = 'Sala'

	name = fields.Char('Nombre')
	number = fields.Integer('Numero')
	descr = fields.Text("Descipción")

	regla_ids = fields.Many2many('acceso.regla', 'sala_ids', string="Reglas", required=False)


class ResGroups(models.Model):
	_inherit = 'res.groups'

	nusuarios = fields.Integer(
		string="Numero de usuarios",
		compute="_compute_nusuarios",
		store=False,
		compute_sudo=False
	)

	regla_ids = fields.One2many('acceso.regla', 'group_id', string="Reglas", required=False)

	@api.depends('users')
	def _compute_nusuarios(self):
		sql = "select uid from res_groups_users_rel where gid = %s"
		params = (self.id,)
		self.env.cr.execute(sql, params)
		result = self.env.cr.fetchall()
		self.nusuarios = len(result)


tipos_reglas = (
	(0, 'PERMITIR'),
	(1, 'DENEGAR')
)
tipos_repeticiones = (
	(0, 'NO'),
	(1, 'SEMANAL'),
	(2, 'MENSUAL'),
	(3, 'ANUAL')
)
dias_semana = (
	(1, 'Lunes'),
	(2, 'Martes'),
	(3, 'Miercoles'),
	(4, 'Jueves'),
	(5, 'Viernes'),
	(6, 'Sábado'),
	(7, 'Domingo')
)
meses = (
	(1, 'Enero'),
	(2, 'Febrero'),
	(3, 'Marzo'),
	(4, 'Abril'),
	(5, 'Mayo'),
	(6, 'Junio'),
	(7, 'Julio'),
	(8, 'Agosto'),
	(9, 'Septiembre'),
	(10, 'Octubre'),
	(11, 'Noviembre'),
	(12, 'Diciembre')
)

class Regla(models.Model):
	_name = 'acceso.regla'

	name = fields.Char("Regla", required=True)
	descr = fields.Text("Descripcion")

	group_id = fields.Many2one('res.groups', string="Grupo")
	sala_ids = fields.Many2many('acceso.sala', string="Salas", required=False)

	dia_hora_ini = fields.Datetime("Desde", required=True)
	dia_hora_fin = fields.Datetime("Hasta", required=False)
	tipo = fields.Selection(tipos_reglas, required=True, string="Tipo")
	repetir = fields.Selection(tipos_repeticiones, string="Repetir", required=True, default=0)
	
	mes = fields.Selection(meses, required=False, string="Mes")
	dia_mes = fields.Integer(required=False, string="Día del mes", default=1)
	dia_semana = fields.Selection(dias_semana, required=False, string="Día de la semana")
	hora = fields.Integer(required=False, string="Hora")
	minuto = fields.Integer(required=False, string="Minuto")


	@api.constrains('dia_mes')
	def _check_dia_mes(self):
		if not 1 <= self.dia_mes <= 31:
			raise models.ValidationError('Día del mes inválido')
	
	@api.constrains('hora')
	def _check_hora(self):
		if not 0 <= self.hora <= 23:
			raise models.ValidationError('Hora inválida')
	
	@api.constrains('minuto')
	def _check_minuto(self):
		if not 0 <= self.minuto <= 59:
			raise models.ValidationError('Minuto inválido')
	
	def testDiaHora(self, datetime):
		testDate = str(datetime)
		_logger.info("BUDEBUUUG")
		_logger.info(type(self.search([('dia_hora_ini', '<=', testDate)])))


class Acceso(models.Model):
	_name = 'acceso.acceso'

	name = fields.Char()

	user_id = fields.Many2one('res.partner', string="Usuario", required=True)
	sala_id = fields.Many2one('acceso.sala', stirng="Sala", required=True)

	@api.model
	def create(self, vals):
		crear = super(Acceso, self).create(vals)
		puede = False
		
		# Buscamos las relgas que se pueden aplicar
		reglasAplicables = []
		for regla in self.sala_id.regla_ids:
			# Comprobamos el día y la hora
			flagHora = False
			regla.testDiaHora(datetime.datetime.now())

			# Comprobamos el usuario
			flagUser = False
			if self.user_id.has_group(regla.group_id):
				flagUser = True

			if flagUser and flagHora:
				reglasAplicables.append(regla)
		
		for regla in reglasAplicables:
			if regla.tipo == 1:			# Si alguna regla impide el acceso no se comprueba más
				puede = False
				break
			# Ahora compro

		if not puede:
			raise models.ValidationError('Acceso denegado')
		else:
			return crear
