def crearLista(cantidadElementos):
	return [None]*cantidadElementos
	
def asignarElementosLista(desde, cantidad, valor, lista):
	for x in range(cantidad):
		lista[x + desde] = valor
		
		
def determinarIndicePPS(indice, medicion, indiceMedicion, pps):
	indicePPS = {'indiceMedicion': indiceMedicion}

	if (indice == 0):
		indicePPS['indicePPS'] = 0
	elif (indice == len(pps)):
		indicePPS['indicePPS'] = indice - 1
	elif(abs(pps[indice] - medicion) < abs(pps[indice - 1] - medicion)):
		indicePPS['indicePPS'] = indice
	else:
		indicePPS['indicePPS'] = indice - 1
		
	return indicePPS
	
def calcularFda(datos):
	offsetOrdenados = sorted([abs(x) for x in datos])

	integral = []
	minimo = min(offsetOrdenados)
	actual = 0
	
	for valor in offsetOrdenados:
		actual += valor
		integral.append(actual)
		
	maximo = max(offsetOrdenados)
	
	integral = [maximo * x/integral[-1] for x in integral]

	return integral
