def recorte(valor):
		valor = str(valor)
		nuevoValor = 0
		for n in valor:
			nuevoValor+=int(n) 
		if len(str(nuevoValor))!=1:
			return recorte(nuevoValor)
		else:
			return nuevoValor

print recorte(394)