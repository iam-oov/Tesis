from CONEXION.BDCone import BDCone

class AreaBD():
	def __init__(self, con):
		''' Campos de la tabla '''
		self.nombreTabla = 'area'
		self.area = ''
		self.db = BDCone(con) # instanciamos la conexion

	def agregar(self):
		query = 'INSERT INTO '+self.nombreTabla+ ' VALUES("'+self.area+'")'
		self.db.ejecutar(query)

	def borrar(self):
		''' Elimina un registro de la tabla '''
		query = 'DELETE FROM '+self.nombreTabla+ ' WHERE area="'+self.area+'"'
		self.db.ejecutar(query)

	def ejecutarQueryDinamico(self, query):
		return self.db.ejecutar(query)

	def leer(self, columna):
		query = 'SELECT '+columna+' FROM '+self.nombreTabla
		return self.db.ejecutar(query)

	