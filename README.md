# Control de Acceso

Este módulo de Odoo permite controlar y registrar el acceso de personas a diferentes salas.

## Funcionamiento

 * Se registran grupos (_GrupoAcceso_) y salas (_Sala_)
 * Se configuran los grupos que pueden acceder a cada sala.
 * Se puede ajustar según día y hora

## Detalles de implementación

### Modelos

 * _GrupoAcceso_ hereda de _res.groups_
 * _GrupoAcceso_ contiene una lista de _res.partner_
 * _Sala_ es un modelo base.
 * _ControlAcceso_ almacena los datos de acceso
	* _GrupoAcceso_
	* _Sala_
	* DiaHora de inicio
	* DiaHora de fin (puede ser nulo)
	* Tipo (Permitir / Denegar)
	* Repetir (No, Semanal, Mensual, Anual)
	* {Los siguientes campos solo se muestran cuando corresponde según el valor de _Repetir_}
		* DiaSemana (null)
		* DiaMes (null)
		* Mes (null)
		* Hora (null)
		* Minuto (null)

### Acciones

 * Configuracion general
 * Solicitar entrada (_GrupoAcceso_, _Sala_)
 * Ver acceso efectivo (_GrupoAcceso_, _Sala_)