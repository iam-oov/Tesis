from CONEXION.BDCone import BDCone

class OrtodoncistaBD():
	def __init__(self, con):
		''' Campos de la tabla '''
		self.nombreTabla = 'ortodoncista'
		self.nombre = ''
		self.apPaterno = ''
		self.apMaterno = ''
		self.telefono = ''
		self.area = ''
		self.db = BDCone(con) # instanciamos la conexion

	def actualizar(self, columna, valor):
		''' Actualiza la tabla que recibe como parametro'''
		query = 'UPDATE '+self.nombreTabla+' SET '+columna+'="'+valor+'" WHERE nombre=%s AND apPaterno=%s AND apMaterno=%s AND telefono=%s AND area=%s' 
		valores = (
			self.nombre,
			self.apPaterno,
			self.apMaterno,
			self.telefono,
			self.area
			)
		print query
		print valores
		return self.db.ejecutar(query, valores)

	def agregar(self):
		query = 'INSERT INTO '+self.nombreTabla+ ' VALUES(%s, %s, %s, %s, %s)'
		valores = (
			self.nombre,
			self.apPaterno,
			self.apMaterno,
			self.telefono,
			self.area
			)
		self.db.ejecutar(query, valores)

	def borrar(self):
		''' Elimina un registro de la tabla '''
		query = 'DELETE FROM '+self.nombreTabla+ ' WHERE nombre=%s AND apPaterno=%s AND apMaterno=%s AND telefono=%s AND area=%s' 
		valores = (
				self.nombre,
				self.apPaterno,
				self.apMaterno,
				self.telefono,
				self.area
			)
		self.db.ejecutar(query, valores)
	
	def leer(self, columna):
		query = 'SELECT '+columna+' FROM '+self.nombreTabla
		return self.db.ejecutar(query)

	def ejecutarQueryDinamico(self, query):
		return self.db.ejecutar(query)

