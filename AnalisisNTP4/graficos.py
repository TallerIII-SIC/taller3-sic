from nucleo import calcularFda

def graficarFda(datos, plt, etiqueta, longitud):
	fda = calcularFda(datos)
	longitudFda = len(fda)
	x = fda[:]
	y = [x/longitudFda for x in range(longitudFda)]
	plt.plot(x, y, label = etiqueta)
	
