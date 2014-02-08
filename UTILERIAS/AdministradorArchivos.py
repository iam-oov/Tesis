from pyDes import des

class AdministradorArchivos():
	''' Esta clase se encarga de leer un archivo .txt '''
	
	def leer(self, ruta, nombreArchivo):
		''' Lee un archivo y regresa su contenido sin saltos de linea. '''
		archivo = open(ruta+nombreArchivo, 'r')
		pacientes = list()

		for linea in archivo.readlines():
			if linea: # ignoramos las lineas vacias
				linea = linea.strip()
				pacientes.append(linea)
		return pacientes

	def parsearLista(self, pacientes, separador=";"):
		''' Este metodo recibe el contenido del archivo(formato de comas)
		y regresa el contenido en una lista con los elementos separados '''
		for datos in pacientes:
			datos = datos.split(separador)
			yield datos

	def parsearCadena(self, cadena, separador='|'):
		cadena = cadena.split(separador)
		return cadena


	def desencriptaFichero(self, contrasena, ruta, nombreArchivo):
	    # abrimos el arhivo, lo guardamos en memoria y cerramos.
	    f = open(ruta+nombreArchivo, 'rb')
	    d = f.read()
	    f.close()

	    # convertimos la clave string en objeto clave
	    k = des(contrasena)

	    #desencriptamos el fichero-objeto en memoria con el
	    #objeto clave y lo grabamos en memoria
	    d = k.decrypt(d, ' ')
	    return d
			



