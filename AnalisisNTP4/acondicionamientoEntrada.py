from bisect import bisect_left
from nucleo import *

def asignarMedicionesPPS(tiempos, pps):
	indices = crearLista(len(tiempos))
	i = 0
	
	for indiceMedicion, medicion in enumerate(tiempos):
		indice = bisect_left(pps, medicion)
		indices[i] = determinarIndicePPS(indice, medicion, indiceMedicion, pps)
		i += 1	
		
	return indices
	
def expandirMediciones(indices, phiReales, phiLocales, phiAjustados):
	indices.sort(key = lambda x: (x['indicePPS']))
	
	primeraPosicion = indices[0]['indicePPS']

	phiRealesAcortada = phiReales[primeraPosicion:]	

	phiLocalesExtendido = crearLista(len(phiRealesAcortada))
	phiAjustadosExtendido = crearLista(len(phiRealesAcortada))
	
	indiceAnterior = None
	
	for indice in indices:	
	
		if(indiceAnterior != None):	
			cantidadElementos = indice['indicePPS'] - indiceAnterior['indicePPS']
		
			asignarElementosLista(	indiceAnterior['indicePPS'] - primeraPosicion, 
									cantidadElementos, 
									phiLocales[indiceAnterior['indiceMedicion']], 
									phiLocalesExtendido)
									
			asignarElementosLista(	indiceAnterior['indicePPS'] - primeraPosicion, 
									cantidadElementos, 
									phiAjustados[indiceAnterior['indiceMedicion']], 
									phiAjustadosExtendido)
		
		indiceAnterior = indice
		
	cantidadElementos = len(phiRealesAcortada) - indiceAnterior['indicePPS'] 
		
	asignarElementosLista(	indiceAnterior['indicePPS'] - primeraPosicion, 
							cantidadElementos, 
							phiLocales[indiceAnterior['indiceMedicion']], 
							phiLocalesExtendido)
									
	asignarElementosLista(	indiceAnterior['indicePPS'] - primeraPosicion, 
							cantidadElementos, 
							phiAjustados[indiceAnterior['indiceMedicion']], 
							phiAjustadosExtendido)
							
	return phiRealesAcortada, phiLocalesExtendido, phiAjustadosExtendido
		