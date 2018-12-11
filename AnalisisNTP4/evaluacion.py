from bisect import bisect_left
from nucleo import *
import math
import time

# A partir de una indiceInicial devuelve el indiceFinal que esta 'anchoVentana' en segundos mas adelante
def determinarIndiceFinalIntervalo(phiReales, indiceInicial, anchoVentana):
	tiempoVentana = 0
	indiceFinal = indiceInicial
	
	longitudPhiReales = len(phiReales)
	

	while (	tiempoVentana < anchoVentana and 
			indiceFinal < longitudPhiReales):
		tiempoVentana += phiReales[indiceFinal] + 1
		indiceFinal += 1
		
	return indiceFinal
		

def calcularMTIEIntervalo(tRelativo, anchoVentana, phiReales, TE, pps):
	#Para obtener el tAbsoluto hay que desplazarlo a partir del inicio de las mediciones
	tAbsoluto =  pps[0] + tRelativo
	
	indiceInicial = bisect_left(pps, tAbsoluto)
		
	indiceInicial = determinarIndicePPS(indiceInicial, tAbsoluto, tAbsoluto, pps)['indicePPS']
	indiceFinal = determinarIndiceFinalIntervalo(phiReales, indiceInicial, anchoVentana)
	
	maximo = max(TE[indiceInicial:indiceFinal])
	minimo = min(TE[indiceInicial:indiceFinal])
	
	return maximo - minimo

def calcularMTIE(anchoVentana, phiReales, TE, pps, desplazamientoVentana = 1):

	#Como es el pps se asume que hay un elemento por segundo.
	cantidadElementos = math.floor(len(pps) / desplazamientoVentana)
	MTIE = crearLista(cantidadElementos)
	
	for i in range(0, cantidadElementos):
		#tRelativo es porque no empieza en el timestamp 0 el pps
		tRelativo = i * desplazamientoVentana
		MTIE[i] = calcularMTIEIntervalo(tRelativo, anchoVentana, phiReales, TE, pps) / anchoVentana
		
	return MTIE