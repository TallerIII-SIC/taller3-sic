def obtenerPPS(nombreArchivo):
	pps = []
	phiReales = []
	guardarResultados = True
	
	ppsAnterior = None;
	ppsActual = None;
	umbral = 10e-4
	
	with open(nombreArchivo) as archivo:
		for linea in archivo:
            
            # Salta las lineas iniciales.
			if not linea[0].isdigit():
				continue
				
			linea = linea[:-1]
			ppsActual = float(linea)
			
			if ppsAnterior != None:
				phiReal = abs(ppsActual - ppsAnterior - 1)
				
				# No guarda los phiReal mas alejados que 10e-4
				if(guardarResultados == False and phiReal <= umbral):
					guardarResultados = True
				elif (guardarResultados == True and phiReal > umbral):
					guardarResultados = False
				
				if(guardarResultados == True):
					pps.append(ppsActual)
					phiReales.append(phiReal)

			ppsAnterior = ppsActual
			
	return pps, phiReales

def obtenerMediciones(nombreArchivo):
	phiLocales = []
	phiAjustados = []
	tiempos = []
	rtts = []
	
	with open(nombreArchivo) as archivo:
		for linea in archivo:
			# Retirar \n
			linea = linea[:-1]

			# Saltear las lineas de encabezado
			if not linea[0].isdigit():
				continue

			# Desempacar los datos
			t1, t2, t3, t4, offset1, offset2 = linea.split(',')
			
			t1 = float(t1);
			
			tiempos.append(t1)
			phiLocales.append(float(offset2))
			phiAjustados.append(float(offset1))
			rtts.append(float(t4) - float(t1))
			
			
	return tiempos, phiLocales, phiAjustados, rtts
