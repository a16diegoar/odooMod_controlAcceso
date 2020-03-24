# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sala(models.Model):
	_name = 'acceso.sala'
	_description = 'Sala'

	name = fields.Char('Nombre')
	number = fields.Integer('Numero')
	descr = fields.Text("Descipción")

	accesos_ids = fields.Many2many('acceso.regla', string="Accesos")


class GrupoAcceso(models.Model):
	_inherit = 'res.groups'

	_name = 'acceso.grupo'


class Regla(models.Model):
	_name = 'acceso.regla'

	name = fields.Char("Regla")
	description = fields.Text("Descripcion")

	salas = fields.Many2many('acceso.sala')
	