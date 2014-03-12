from CONEXION.BDCone import BDCone

class Ortodoncista():
	def __init__(self, con):
		''' Campos de la tabla '''
		self.nombreTabla = 'ortodoncista'
		self.nombre = ''
		self.apPaterno = ''
		self.apMaterno = ''
		self.telefono = ''
		self.area = ''
		self.db = BDCone(con) # instanciamos la conexion

	
	def leer(self, columna):
		query = 'SELECT '+columna+' FROM '+self.nombreTabla+' ORDER BY '+columna+' ASC'
		return self.db.ejecutar(query)