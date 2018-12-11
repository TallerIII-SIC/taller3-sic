import numpy as np
import matplotlib.pyplot as plt

from main import calculate_cdf

def main():
	phi_values = []
	with open('pps.log') as file:
		previous = None
		for line in file:
			line = line[:-1]
			current_pps = float(line)
			if previous != None:
				#cortar lo que está arriba de "10e-4" (ver qué valor corresponde)
				diff = current_pps - previous - 1
				phi_values.append(abs(diff)) 

			previous = current_pps


	plt.plot(phi_values, 'o')
	#cdf = calculate_cdf(phi_values)
	#plt.plot(cdf, [x/len(cdf) for x in range(len(cdf))], '.')
	plt.show()



def foo():
	# pasarle bins logarítmicos
	hist, bin_edges = np.histogram(phi_values, bins=100, normed=True)
	print(hist)
	print(bin_edges)
	plt.plot(np.cumsum(hist))
	plt.show()


if __name__ == '__main__':
	main()
