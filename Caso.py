import random

class Caso():
	def __init__(self):
		self.cargarCasos()

	def cargarCasos(self):
		self._casos = ['caso 1', 'caso 2', 'caso 3']

	def seleccionarCaso(self):
		return random.choice(self.casos)

	@property
	def casos(self):
		return self._casos




