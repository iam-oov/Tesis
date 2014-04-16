from CONEXION.BDCone import BDCone

class HistorialBD():
	def __init__(self, con):
		''' Campos de la tabla '''
		self.nombreTabla = 'historial'
		self.id = 0
		self.casoAnterior = ''
		self.casoNuevo = ''
		self.fecha = ''
		self.ortodoncista = ''
		self.comentario = ''
		self.rutaCasoAnterior = ''
		self.rutaCasoNuevo = ''
		self.db = BDCone(con) # instanciamos la conexion

	
	def leer(self, columna):
		query = 'SELECT '+columna+' FROM '+self.nombreTabla+' ORDER BY '+columna+' ASC'
		return self.db.ejecutar(query)

	def obtenerCasoAnterior(self, id):
		query = 'SELECT casoNuevo, rutaCasoNuevo'+' FROM '+self.nombreTabla+\
		' WHERE id="'+id+'" ORDER BY fecha DESC LIMIT 1'
		return self.db.ejecutar(query)

	def obtenerHistorial(self, id):
		query = 'SELECT casoNuevo, rutaCasoNuevo'+' FROM '+self.nombreTabla+\
		' WHERE id="'+id+'"'
		return self.db.ejecutar(query)

	def agregar(self):
		query = 'INSERT INTO '+self.nombreTabla+ ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
		valores = (
				self.id,
				self.casoAnterior,
				self.casoNuevo,
				self.fecha,
				self.ortodoncista,
				self.comentario,
				self.rutaCasoAnterior,
				self.rutaCasoNuevo
			)
		self.db.ejecutar(query, valores)