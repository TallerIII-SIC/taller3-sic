# -*- coding: utf-8 -*-

from decimal import *
import matplotlib.pyplot as pl 
import numpy as np
import sys
import os
from collections import MutableSequence
from scipy.linalg.blas import dgemm
from datetime import datetime

directorio_actual=os.getcwd()
ruta=directorio_actual + "/"
log_cliente="TE_600.txt"

global archivo
global fi_estimado_a
global fi_real_a
global fi_error_a
global timestamp_a

archivo= ruta+log_cliente
fi_estimado_a = np.array([])      	
fi_real_a	 = np.array([])		
fi_error_a    = np.array([])		
timestamp_a   = np.array([])


def leer_datos(time_calc, file_name, d):

	global archivo
	global fi_estimado_a
	global fi_real_a
	global fi_error_a
	global timestamp_a
	
	tiempo_calculo=time_calc			# Esta variable define los limites del error medido

	tiempo_i=datetime.now()
	print tiempo_i

	largo=len(timestamp_a)
	print "Carga completa %s registros"%(largo) 
	f=open(ruta+file_name,"a")
	contador=0
	timestamp_new=np.array([]) 
	fi_estimado_new=np.array([]) 
	fi_real_new=np.array([]) 
	fi_error_new=np.array([]) 
	print "Calculando error...."
	for i in range(0,largo):
		timestamp_new=np.append(timestamp_new,timestamp_a[i])
		fi_real_new=np.append(fi_real_new,fi_real_a[i])
		fi_estimado_new=np.append(fi_estimado_new,fi_estimado_a[i])
		fi_error = fi_estimado_a[i] - fi_real_a[i]
		fi_error_new=np.append(fi_error_new,fi_error)
		contador+=1
		if contador==tiempo_calculo:
			referencia=timestamp_new[0]
			minimo=min(fi_error_new)
			maximo=max(fi_error_new)
			val_diferencia=(maximo-minimo)/d
			f.write("%s %s\n"%(referencia,val_diferencia))
			contador=0
			timestamp_new=np.array([]) 
			fi_estimado_new=np.array([]) 
			fi_real_new=np.array([]) 
			fi_error_new=np.array([])	
	f.close()
	print "Calculo completo"

def iniciar():

	global archivo
	global fi_estimado_a
	global fi_real_a
	global fi_error_a
	global timestamp_a


	leer=np.loadtxt(archivo)#,dtype=str)
	print "Cargando...."
	
	for line in leer:
		timestamp    = int(line[0])					
		fi_estimado  = float(line[1])					
		fi_real      = float(line[2])					
		timestamp_a = np.append(timestamp_a,timestamp)				
		fi_estimado_a=np.append(fi_estimado_a,fi_estimado)
		fi_real_a=np.append(fi_real_a,fi_real)
		
iniciar()
leer_datos(60,"log_error_600-1.txt",1)
leer_datos(120,"log_error_600-2.txt",2)
leer_datos(180,"log_error_600-3.txt",3)
leer_datos(300,"log_error_600-5.txt",5)
leer_datos(600,"log_error_600-10.txt",10)
