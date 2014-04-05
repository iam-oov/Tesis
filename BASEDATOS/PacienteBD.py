from CONEXION.BDCone import BDCone

class PacienteBD():
	def __init__(self, con):
		''' Campos de la tabla '''
		self.nombreTabla = 'paciente'
		self.id = 0 
		self.nombre = ''
		self.apPaterno = ''
		self.apMaterno = ''
		self.telefono = ''
		self.ortodoncista = ''
		self.casoActual = ''
		self.rutaImagen = ''
		self.db = BDCone(con) # instanciamos la conexion
	
	def agregar(self):
		query = 'INSERT INTO '+self.nombreTabla+ ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
		valores = (
				self.id,
				self.nombre,
				self.apPaterno,
				self.apMaterno,
				self.telefono,
				self.ortodoncista,
				self.casoActual,
				self.rutaImagen
			)
		self.db.ejecutar(query, valores)

	def borrar(self):
		''' Elimina un registro de la tabla '''
		query = 'DELETE FROM '+self.nombreTabla+ ' WHERE id=%s AND nombre=%s AND apPaterno=%s AND apMaterno=%s AND telefono=%s AND ortodoncista=%s AND casoActual=%s AND rutaImagen=%s' 
		valores = (
				self.id,
				self.nombre,
				self.apPaterno,
				self.apMaterno,
				self.telefono,
				self.ortodoncista,
				self.casoActual,
				self.rutaImagen
			)
		self.db.ejecutar(query, valores)

	def ejecutarQueryDinamico(self, query):
		return self.db.ejecutar(query)

	def leer(self, columna):
		query = 'SELECT '+columna+' FROM '+self.nombreTabla
		return self.db.ejecutar(query)

	def obtenerId(self, nombre):
		query = 'SELECT id FROM '+self.nombreTabla+' WHERE nombre="'+nombre+'"'
		return self.db.ejecutar(query)