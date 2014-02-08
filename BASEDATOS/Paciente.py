from CONEXION.BDCone import BDCone

class Paciente():
	def __init__(self, con):
		''' Campos de la tabla '''
		self.nombreTabla = 'registros'
		self.id = 0 # autoincrementable
		self.nombre = ''
		self.caso = ''
		self.db = BDCone(con) # instanciamos la conexion
	
	def leer(self, columna):
		query = 'SELECT '+columna+' FROM '+self.nombreTabla+' ORDER BY '+columna+' ASC'
		return self.db.ejecutar(query)