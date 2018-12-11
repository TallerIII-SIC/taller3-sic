import numpy as np
import matplotlib.pyplot as plt



	

def main():
	
	
	phiLocales, phiAjustados = expandirMediciones(tiempos, pps, phiLocales, phiAjustados)
	

	#print("Minimum RTT:", min(rtts))
	#print("Maximum RTT:", max(rtts))
	#cdf_1 = calculate_cdf(offsets_1)
	#cdf_2 = calculate_cdf(offsets_2)

	#for n, v in enumerate(cdf_2):
	#	print("{}: {}".format(n, v))
		
	#plt.plot(cdf_1, [x/len(cdf_1) for x in range(len(cdf_1))])
	#plt.plot(cdf_2, [x/len(cdf_2) for x in range(len(cdf_2))])
	#plt.show()




if __name__ == '__main__':
	main()
