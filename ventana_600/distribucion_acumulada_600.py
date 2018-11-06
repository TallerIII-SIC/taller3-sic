# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np

print(matplotlib.__version__)
ruta=os.getcwd()+"/"
#archivos=np.array(["log_error_120-1.txt","log_error_120-2.txt","log_error_120-3.txt","log_error_120-5.txt","log_error_120-10.txt"])
archivos=np.array(["log_error_600-1.txt","log_error_600-2.txt","log_error_600-3.txt","log_error_600-5.txt","log_error_600-10.txt"])

#linea_estilo = ['.', ':', '-.', ':','-']
linea_estilo = ['-', '-', '-', '-','-']

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 20,
        }

title_font = {'family':'serif', 'size':24, 'color':'black', 'weight':'normal','verticalalignment':'bottom'}

#plt.title("Ventana 120 segundos",fontdict=title_font)
colores=np.array(['green', 'yellow', 'sienna', 'gold', 'tomato'])
#axis_font = {'family':'serif', 'size':20}
axis_font = {'family':'serif', 'size':24}
plt.ylabel("Frecuencia", fontdict=axis_font)
plt.xlabel("MTIE [us]", fontdict=axis_font)
#plt.tick_params(labelsize=18)
plt.tick_params(labelsize=22)
plt.xlim([0.5,210.00])
plt.grid(b=True, which='both', color='0.05', linestyle='-', alpha = 0.05)
#plt.legend(handles=[red_patch], labels = [''])


def crea_arreglos(archivo, valor):
	
	leer=np.loadtxt(archivo, usecols = 1, dtype = float)
	#leer.astype(np.int64)
	leer.sort()

	datos=leer
	#frecuencia=np.array([])

	l=datos.size
	frecuencia=np.array([])
	frecuencia=np.append(frecuencia,float(1)/l)

	for i in range(2,l+1):
		frecuencia=np.append(frecuencia,float(1)/l+frecuencia[i-2])
		
	Ymin=np.min(frecuencia)
	Ymax=np.max(frecuencia)
	p90x=np.percentile(datos,90)
	p90y=np.percentile(frecuencia,90)
	#plt.tick_params(axis="x", pad=8)
	print("Percentil 90 en x %s y en y %s ymin %s ymax %s\n"%(p90x, p90y, Ymin, Ymax))

	if valor==0:
		minuto=60
		plt.vlines(p90x,Ymin,0.9,color='black',label='Percentil 90 : %.5s'%p90x,linestyle='--')
		#plt.vlines(p90x,Ymin,0.9,color='black',label='Percentil 90 : %.5s'%p90x,linestyle='--')
		#plt.hlines(p90y,np.min(datos), p90x,color='black',linestyle='--')
		plt.hlines(p90y,2.00, p90x,color='black',linestyle='--')
		#plt.grid(axis='x')
	elif valor==1:
		minuto=120
	elif valor==2:
		minuto=180
	elif valor==3:
		minuto=300
	elif valor==4:
		minuto=600

	plt.semilogx(datos,frecuencia, color = '%s'%(colores[valor]), linestyle = '%s'%(linea_estilo[valor]),lw=2,label='S: %s segundos'%(minuto))
	#plt.plot(datos,frecuencia,'%s%s'%(colores[valor],linea_estilo[valor]),label='%s minutos'%(minuto))

	
	return


def iniciar():
	
	for i , leer in enumerate (archivos,start=0):
		crea_arreglos(leer, i)
	
	plt.legend(loc='center right',prop={'size':20}, fancybox=True) #,labels = [''])		
	plt.show()
		
iniciar()
