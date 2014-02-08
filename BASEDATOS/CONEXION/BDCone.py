import MySQLdb

# tenemos que hacer que los datos para las conexiones sean dinamicas, 
'''
Lee de un archivo encriptado las credenciales
'''

class BDCone:
    def __init__(self, con):
        self.db_host = con[0]
        self.db_usuario = con[1]
        self.db_contrasena = con[2]
        self.db_nombre = con[3]

    def conectar(self):
        self.db = MySQLdb.connect(host=self.db_host, user=self.db_usuario,
                                  passwd=self.db_contrasena, db=self.db_nombre)

    def abrirCursor(self):
        self.cursor = self.db.cursor()

    def ejecutarConsulta(self, query, valors=''):
        if valors != '':
            self.cursor.execute(query, valors)
        else:
            self.cursor.execute(query)

    def traerDatos(self):
        self.columnas = self.cursor.fetchall()

    def enviarCommit(self, query):
        sql = query.lower()
        lectura = sql.count('select')
        if lectura < 1:
            self.db.commit()

    def cerrarCursor(self):
        self.cursor.close()

    def ejecutar(self, query, valores=''):
        # ejecuta todo el proceso solo si los atributos han sido definidos
        if (self.db_host and self.db_usuario and self.db_contrasena and self.db_nombre and
            query):
            self.conectar()
            self.abrirCursor()
            self.ejecutarConsulta(query, valores)
            self.enviarCommit(query)
            self.traerDatos()
            self.cerrarCursor()
            return self.columnas
