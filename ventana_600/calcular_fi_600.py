# -*- coding: utf-8 -*-

from decimal import *
from collections import MutableSequence
from scipy.linalg.blas import dgemm
from datetime import datetime
import numpy as np
import sys
import os
import ConfigParser
import time

## Obtiene el directorio de archivos
#global ruta 
directorio_actual = os.getcwd()

## Lee datos del archivo de configuracion
config = ConfigParser.ConfigParser()
config.read(directorio_actual+"/configuracion.cfg")
ruta   = directorio_actual
t1_pps = config.get("calcula_error_cfg", "t1_pps")
t2_pps = config.get("calcula_error_cfg", "t2_pps")
log_cliente = config.get("calcula_error_cfg", "log")

## Variables globales
global t1_ref_real_lista
global fi_real_lista
global t1_ref_real
global fi_real
global fi_metodo3_todos
global rtt_todos
global t1_todos
global fi_real
global t1_ref_real
global tiempo_i
global tiempo_f
global primera_recta
global m_ant 
global c_ant 
global alfa 
global m2 
global c2
global primer_rtt_minimo
global ultimo_rtt_minimo
global corte_proceso
global f

## Fin variables globales

##**********************************************************************

class listaCircular(MutableSequence):
	def __init__(self, size):
		## Constructor de la clase
		super(listaCircular, self).__init__()		
		self.index = 0
		self.size = size
		self._data = list()
	def __len__(self):
		return len(self._data)
	def __getitem__(self, ii):
		return self._data[ii]
	def __delitem__(self, ii):
		del self._data[ii]
	def __setitem__(self, ii, val):
		self._data[ii] = val
		return self._data[ii]	
	def insert(self, ii, val):
		self._data.insert(ii, val)        
	def append(self, value):
		## Agregar elemento
		if len(self._data) == self.size:	
			self._data.pop(0)				## Saca el primer valor
			self._data.append(value)		## Agrega un valor al final
		else:
			self._data.append(value)
		self.index = (self.index + 1) % self.size	## El indice siempre será rotatorio hasta la longitud del vector
		
	def getitem(self, key):
		## Devuelve el elemento en base al indice 
		if key < len(self._data): 
			return(self._data[key])
		else:
			return None
			
	def __repr__(self):
		## Devuelve los elementos de la lista
		return self._data.__repr__() 
		
	def getsize(self):
		## Devuelve el largo de la lista
		longitud= len(self._data)
		return longitud

##**********************************************************************

def leer_datos(): 

	global fi_metodo3_todos
	global rtt_todos
	global t1_todos
	global fi_real
	global t1_ref_real
	global tiempo_i
	global corte_proceso
	global t1_ref_real_lista
	global fi_real_lista
	#global t1_ref_real
	#global fi_real	
	
	corte_proceso=0
	t1Pps = []
	t2Pps = []
	t1=[]
	fi_metodo3 = []

	t1Pps_new=[]						
	t2Pps_new=[]						
	t1_new=[]
	fi_metodo3_new=[]
	
	t1PpsFinal=[]
	t2PpsFinal=[]
	t1Final=[]
	fi_metodo3Final=[]
	
	fi_real=np.array([])
	t1_ref_real=np.array([])
		
	## Inicio de lectura DATOS
	tiempo_i=datetime.now()
	print ("Tiempo inicial de calculo: %s"%(tiempo_i)) 
	archivo= ruta + "/" + log_cliente		
	rtt_todos = np.array([])			
	fi_metodo3_todos = np.array([])		
	t1_todos=np.array([])				
	t2_todos=np.array([])				
	leer=np.loadtxt(archivo,dtype=str,delimiter='|')
	print "Lectura de todos los tiempos...."
	for line in leer:
		t1  = int(float(line[0]))					## Tiempo 1
		t2  = int(float(line[1]))					## Tiempo 2
		t3  = int(float(line[2]))					## Tiempo 3
		t4  = int(float(line[3].split('\n')[0]))		## Tiempo 4			
		fi_metodo3_ = float(t1-t2+t4-t3)/2			## fi calculado
		fi_metodo3_todos = np.append(fi_metodo3_todos,fi_metodo3_)
		t1_todos=np.append(t1_todos,int(t1/1e6))	## Tiempo referencial, en segundos
		rtt_todos=np.append(rtt_todos,float(t4-t1))

	## Inicio de lectura datos para los valores de T1_PPS 
	print "Lectura de t1_pps...."
	f1 = open(ruta + "/" + t1_pps, 'r')  	
	t1Pps +=f1.readlines()
	f1.close()

	a=int(t1Pps[0][:10])	## Inicio de archivo
	c=len(t1Pps)
	b=int(t1Pps[c-1][:10])	## Fin de archivo

	largo=len(t1Pps)
	for i in range(a,b+1):
		if (i == int(t1Pps[0][:10])):					
			t1Pps_new.append(t1Pps[0].split('\n')[0])	## Si existe el valor lo agrega al array
			t1Pps.pop(0)								## Luego lo saca
		else:
			t1Pps_new.append('0')
			if(t1Pps[0][:10].split('\n')[0] == '0'):	## Sino agrega un cero
				t1Pps.pop(0)

	## Inicio de lectura datos para los valores de T2_PPS 
	print "Lectura de t2_pps...."	
	f2 = open(ruta + "/" + t2_pps, 'r')  
	t2Pps +=f2.readlines()
	f2.close()

	a=int(t2Pps[0][:10])		
	c=len(t2Pps)
	b=int(t2Pps[c-1][:10])		

	for i in range (a,b+1):									
		if (i == int(t2Pps[0][:10])):	
			t2Pps_new.append(t2Pps[0].split('\n')[0])		
			t2Pps.pop(0)									
		else:
			t2Pps_new.append('0')			
			if(t2Pps[0][:10].split('\n')[0] == '0'):
				t2Pps.pop(0)

	# Verificacion de secuencia de tiempos en datos de pps
	print "Verificacion de secuencia en datos pps...."		
	l=len(t1Pps_new)
	for i in range(0,l):
		if((t1Pps_new[i]=='0') or (t2Pps_new[i]=='0')):  				## Si alguno de los arreglos tiene un cero, lo descarta	
			continue
		else:
			t1PpsFinal.append(t1Pps_new[i])
			t2PpsFinal.append(t2Pps_new[i])
			a=int(float(t1Pps_new[i][:10])*1e6)
			aux_tiempo=int(a/1e6)		 								## Pasa el tiempo a segundos 
			t1_ref_real=np.append(t1_ref_real, float(aux_tiempo))		## Tiempo de referencia
			fi_real_valor=(float(t1Pps_new[i])-float(t2Pps_new[i]))		## Fi real en microsegundos
			
			## Si se observa un cambio en alguno de los relojes hay un desfase, comentar si no existe dicho desfase
			if (fi_real_valor)< 0:
				fi_real_valor = fi_real_valor+1000000
			
			#if (int(t1Pps_new[i][:10]) >= 1507886928 and int(t1Pps_new[i][:10]) <= 1508188083):
				#fi_real_valor = fi_real_valor+1000000
								
			fi_real=np.append(fi_real,(fi_real_valor))					
	
	t1_ref_real_lista=t1_ref_real.tolist()
	fi_real_lista=fi_real.tolist()
    
        copiaaa = np.array(fi_real_lista)

        copiaaa.tofile("FIREAL.bin")

	print "Fin de lectura y ajuste de tiempos"

#***********************************************************************

def procesar_datos():

	#Lista para todos los valores de fi real
	global t1_ref_real_lista
	global fi_real_lista
	global f

	#Datos para la recta de fi calculado
	global primera_recta
	global m_ant
	global c_ant
	global alfa
	global m2
	global c2
	global corte_proceso
	
	#Variables para control de cambio de camino
	global primer_rtt_minimo
	global ultimo_rtt_minimo   
	#global contador
	
	#Arreglos para almacenar datos de la medicion
	
	global rtt_minimo
	global buffer_mediana
	global buffer_minuto_medianas
	global buffer_minuto_tiempos
	global buffer_colector_medianas
	global buffer_colector_tiempos
	
	c_ant=0
	m_ant=0
	c2=0
	m2=0
	primer_rtt_minimo=0
	ultimo_rtt_minimo=0

	alfa=float(0.05)
	porcentaje=0.05
	
	tamanio_mediana=600						## Tamaño de la lista circular (10 minutos)
	tiempo_calculo=61 						## Ventanas de medicion (1 minuto)
	mediana_temporal=0
	rtt_temporal=0
	ventana_rtt=60							## Ventana de rtt para obtener el minimo

	buffer_mediana=listaCircular(tamanio_mediana)
	buffer_minuto_medianas=np.array([])
	buffer_minuto_tiempos =np.array([])	
	buffer_colector_medianas=np.array([])
	buffer_colector_tiempos=np.array([])
	rtt_minimo=np.array([])		
	
	primera_recta=False
	completo_mediana=False
	primera_ventana=False

	print "Ecuacion utilizada -> t4+[(t4-t1)-(t3-t2)]/2-t3)"
	#g=open(ruta +"/"+"desincronizados.txt","a")
	for i in range(corte_proceso,len(fi_metodo3_todos)):		
		valor_phi_estimado=fi_metodo3_todos[i]
		## Condicion para llenar la lista circular
		if completo_mediana == False:									
			buffer_mediana.append(valor_phi_estimado)
			## Agregado para almacenar el rtt
			#------------------------------------------------------------
			if (tamanio_mediana-buffer_mediana.getsize() < ventana_rtt):
				valor_rtt=rtt_todos[i]
				rtt_minimo=np.append(rtt_minimo,valor_rtt)
			#------------------------------------------------------------
			if (buffer_mediana.getsize() == tamanio_mediana):		
				print "Completando %s valores"%(tamanio_mediana)
				completo_mediana=True									## Indica que se lleno la lista circular
				tiempo_inicial=t1_todos[i]+1							## Toma el tiempo inicial de para el calculo
				contador_segundos=0										## Variable para validar la secuencia de tiempos
				primer_rtt_minimo=rtt_minimo.min()
				rtt_minimo=np.array([])
		## Despues de llenar la lista
		else:
			## Condicion para validar el primer minuto
			if primera_ventana == False:
				tiempo_actual=t1_todos[i]
				tiempo_siguiente=tiempo_inicial+contador_segundos		## Variable secuencial de los segundos		
				if (tiempo_actual==tiempo_siguiente):					## Verifica si el valor del tiempo es secuencial
					#*****************************************
					valor_rtt=rtt_todos[i]
					rtt_minimo=np.append(rtt_minimo,valor_rtt)
					rtt_temporal = valor_rtt
					#*****************************************
					valor_phi_estimado=fi_metodo3_todos[i]				
					buffer_mediana.append(valor_phi_estimado)
					tem_mediana=np.asarray(buffer_mediana)				## Convierte la lista en np.array para obtener la mediana
					mediana=np.median(tem_mediana)					
					buffer_minuto_medianas=np.append(buffer_minuto_medianas,mediana)				## Agrega al array de medianas
					buffer_minuto_tiempos=np.append(buffer_minuto_tiempos,tiempo_actual)			## Agrega el tiempo de referencia
					mediana_temporal=mediana							## Mantiene el valor en memoria
					contador_segundos+=1								## Incrementa la secuencia de segundos

					if (buffer_minuto_tiempos.size==tiempo_calculo):	## Compara si cumplio el tiempo de estimacion
						primera_ventana=True							# Indica que ya pasa el primer minuto
						primera_recta=True								# Indica que es la primera recta
						#**************************************************
						ultimo_rtt_minimo=rtt_minimo.min()
						diferencia=ultimo_rtt_minimo-primer_rtt_minimo
						if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo)) and (abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
							corte_proceso=i
							print "Cambia la ruta 1 %s"%(corte_proceso)
							del(buffer_mediana)
							return 
						primer_rtt_minimo=ultimo_rtt_minimo
						rtt_minimo=np.array([])
						#**************************************************
						procesar_informacion(buffer_minuto_tiempos, buffer_minuto_medianas)	## Envia los datos del minuto a procesar
						buffer_minuto_tiempos=np.array([])
						buffer_minuto_medianas=np.array([])
						contador_segundos=0								## Vuelve a iniciar el contador de segundos
						tiempo_inicial=tiempo_actual+1					## Indica el tiempo inicial igual el tiempo que cierra el minuto
				elif (tiempo_actual > tiempo_siguiente ):				## Si no es secuencial coloca el valor anterior
					relleno=int(tiempo_actual-tiempo_siguiente)			## Cantidad de segundos a completar
					for x in range(0, relleno):
						if (buffer_minuto_tiempos.size==tiempo_calculo):
							primera_ventana=True
							primera_recta=True
							#************************************************
							ultimo_rtt_minimo=rtt_minimo.min()
							diferencia=ultimo_rtt_minimo-primer_rtt_minimo
							if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo))and(abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
								corte_proceso=i
								del(buffer_mediana)
								return
							primer_rtt_minimo=ultimo_rtt_minimo							
							rtt_minimo=np.array([])
							#************************************************
							procesar_informacion(buffer_minuto_tiempos, buffer_minuto_medianas)
							buffer_minuto_tiempos=np.array([])
							buffer_minuto_medianas=np.array([])							
							contador_segundos=0	
							tiempo_inicial=tiempo_siguiente+x-1  ##
						#****************************************
						if (mediana_temporal == 0):
							print "1- %s Aqui la mediana le asigna 0" %(i)
							tem_mediana=np.asarray(buffer_mediana)				## Convierte la lista en np.array para obtener la mediana
							mediana=np.median(tem_mediana)
						#*****************************************			
						buffer_colector_medianas=np.append(buffer_minuto_medianas,mediana_temporal)
						buffer_colector_tiempos=np.append(buffer_minuto_tiempos,tiempo_siguiente+x)
						# Esto porque justo coincide en el cambio
						if rtt_temporal == 0:
							rtt_temporal=rtt_todos[i]
							print "Aqui vale 0 y agregamos %s %s"%(rtt_temporal,tiempo_siguiente+x)
							#************************************************
						rtt_minimo=np.append(rtt_minimo,rtt_temporal)
							#************************************************
						contador_segundos+=1
					if (buffer_minuto_tiempos.size==tiempo_calculo):
						primera_ventana=True
						primera_recta=True
						#************************************************
						ultimo_rtt_minimo=rtt_minimo.min()
						diferencia=ultimo_rtt_minimo-primer_rtt_minimo
						if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo))and(abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
							corte_proceso=i
							del(buffer_mediana)
							return
						primer_rtt_minimo=ultimo_rtt_minimo							
						rtt_minimo=np.array([])
						#************************************************						
						procesar_informacion(buffer_minuto_tiempos, buffer_minuto_medianas)
						buffer_minuto_tiempos=np.array([])
						buffer_minuto_medianas=np.array([])
						contador_segundos=0							
						tiempo_inicial=tiempo_siguiente+x	##
					#*****************************************
					valor_rtt=rtt_todos[i]
					rtt_minimo=np.append(rtt_minimo,valor_rtt)
					rtt_temporal = valor_rtt
					#*****************************************
					valor_phi_estimado=fi_metodo3_todos[i]
					buffer_mediana.append(valor_phi_estimado)
					tem_mediana=np.asarray(buffer_mediana)
					mediana=np.median(tem_mediana)					
					buffer_minuto_medianas=np.append(buffer_minuto_medianas,mediana)
					buffer_minuto_tiempos=np.append(buffer_minuto_tiempos,tiempo_actual)
					mediana_temporal=mediana
					contador_segundos+=1	
					if (buffer_minuto_tiempos.size==tiempo_calculo):
						primera_ventana=True
						primera_recta=True
						#************************************************
						ultimo_rtt_minimo=rtt_minimo.min()
						diferencia=ultimo_rtt_minimo-primer_rtt_minimo
						if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo))and(abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
							corte_proceso=i
							del(buffer_mediana)
							return
						primer_rtt_minimo=ultimo_rtt_minimo							
						rtt_minimo=np.array([])
						#************************************************				
						procesar_informacion(buffer_minuto_tiempos, buffer_minuto_medianas)	
						buffer_minuto_tiempos=np.array([])
						buffer_minuto_medianas=np.array([])						
						contador_segundos=0								
						tiempo_inicial=tiempo_actual+1					
				else:
					print "Error en log de datos"
					sys.exit()
			else:
				##******************************************************************************************************
				## Despues del primer minuto
				tiempo_actual=t1_todos[i]	
				tiempo_siguiente=tiempo_inicial+contador_segundos	
				if (tiempo_actual==tiempo_siguiente):
					#*****************************************
					valor_rtt=rtt_todos[i]
					rtt_minimo=np.append(rtt_minimo,valor_rtt)
					rtt_temporal = valor_rtt
					#*****************************************								
					valor_phi_estimado=fi_metodo3_todos[i]
					buffer_mediana.append(valor_phi_estimado)
					tem_mediana=np.asarray(buffer_mediana)				
					mediana=np.median(tem_mediana)					
					buffer_colector_medianas=np.append(buffer_colector_medianas,mediana)
					buffer_colector_tiempos=np.append(buffer_colector_tiempos,tiempo_actual) 
					mediana_temporal=mediana							
					contador_segundos+=1					
					if (buffer_colector_tiempos.size==tiempo_calculo):	
						#**************************************************
						ultimo_rtt_minimo=rtt_minimo.min()
						diferencia=ultimo_rtt_minimo-primer_rtt_minimo
						if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo)) and (abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
							corte_proceso=i
							del(buffer_mediana)
							return
						primer_rtt_minimo=ultimo_rtt_minimo
						rtt_minimo=np.array([])
						#**************************************************						
						procesar_informacion(buffer_colector_tiempos, buffer_colector_medianas)
						buffer_colector_tiempos=np.array([])
						buffer_colector_medianas=np.array([])						
						contador_segundos=0									
						tiempo_inicial=tiempo_actual+1
				elif (tiempo_actual > tiempo_siguiente ):					
					relleno=int(tiempo_actual-tiempo_siguiente)	
					for x in range(0, relleno):
						if (buffer_colector_tiempos.size==tiempo_calculo):
							#************************************************
							ultimo_rtt_minimo=rtt_minimo.min()
							diferencia=ultimo_rtt_minimo-primer_rtt_minimo
							if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo))and(abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
								corte_proceso=i
								del(buffer_mediana)
								return
							primer_rtt_minimo=ultimo_rtt_minimo							
							rtt_minimo=np.array([])
							#************************************************
							procesar_informacion(buffer_colector_tiempos, buffer_colector_medianas)	
							buffer_colector_medianas=np.array([])
							buffer_colector_tiempos=np.array([])							
							contador_segundos=0	
							tiempo_inicial=(tiempo_siguiente+x)-1 ##
						if (mediana_temporal == 0):
							print "1- %s Aqui la mediana le asigna 0" %(i)
						buffer_colector_medianas=np.append(buffer_colector_medianas,mediana_temporal)
						buffer_colector_tiempos=np.append(buffer_colector_tiempos,tiempo_siguiente+x) ###
						#************************************************
						rtt_minimo=np.append(rtt_minimo,rtt_temporal)
						#************************************************
						contador_segundos+=1
					if (buffer_colector_tiempos.size==tiempo_calculo):
						#************************************************
						ultimo_rtt_minimo=rtt_minimo.min()
						diferencia=ultimo_rtt_minimo-primer_rtt_minimo
						if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo))and(abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):							#f.write("%s|%s\n"%(buffer_colector_tiempos[0],ultimo_rtt_minimo))
							corte_proceso=i
							del(buffer_mediana)
							return
						primer_rtt_minimo=ultimo_rtt_minimo							
						rtt_minimo=np.array([])
						#************************************************							
						procesar_informacion(buffer_colector_tiempos, buffer_colector_medianas)	
						buffer_colector_medianas=np.array([])
						buffer_colector_tiempos=np.array([])						
						contador_segundos=0								
						tiempo_inicial=tiempo_siguiente+x ####
					#*****************************************
					valor_rtt=rtt_todos[i]
					rtt_minimo=np.append(rtt_minimo,valor_rtt)
					rtt_temporal = valor_rtt
					#*****************************************
					valor_phi_estimado=fi_metodo3_todos[i]
					buffer_mediana.append(valor_phi_estimado)
					tem_mediana=np.asarray(buffer_mediana)
					mediana=np.median(tem_mediana)	
					mediana_temporal=mediana				
					buffer_colector_medianas=np.append(buffer_colector_medianas,mediana)
					buffer_colector_tiempos=np.append(buffer_colector_tiempos,tiempo_actual)
					contador_segundos+=1	
					if (buffer_colector_tiempos.size==tiempo_calculo):
						#************************************************
						ultimo_rtt_minimo=rtt_minimo.min()
						diferencia=ultimo_rtt_minimo-primer_rtt_minimo
						if((abs(diferencia)>abs(porcentaje*primer_rtt_minimo))and(abs(diferencia)>abs(porcentaje*ultimo_rtt_minimo))):
							corte_proceso=i
							del(buffer_mediana)
							return
						primer_rtt_minimo=ultimo_rtt_minimo							
						rtt_minimo=np.array([])
						#************************************************
						procesar_informacion(buffer_colector_tiempos, buffer_colector_medianas)	
						buffer_colector_medianas=np.array([])
						buffer_colector_tiempos=np.array([])						
						contador_segundos=0								
						tiempo_inicial=tiempo_actual+1
				else:
					print "Segundo duplicado o incorrecto (tiempo anterior %s tiempo siguiente %s)"%(tiempo_actual, tiempo_siguiente)
					sys.exit()				
	## Si quedaron datos por procesar
	if (buffer_colector_medianas.size > 0):
		procesar_informacion(buffer_colector_tiempos, buffer_colector_medianas)
		tiempo_f=datetime.now()
		total=tiempo_f-tiempo_i
		print ("Calculo completo")
		print ("Finaliza el calculo a las %s"%(tiempo_f))
		print ("Tiempo total de procesamiento %s"%(total))
		sys.exit()
#***********************************************************************

def procesar_informacion(tr, medianas):

	tr_ajustado, phi_ajustado = calcular_recta(tr, medianas)
	if primera_recta == False and len(tr_ajustado) > 0:
		## Tiempo inicio y fin para extraer el correspondiente de fi real para hacer las diferencias
		tiempo_inicio=np.min(tr_ajustado)				    
		tiempo_fin   =np.max(tr_ajustado)
		tr_real_acotado, fi_real_acotado = obtener_fi_real(int(tiempo_inicio), int(tiempo_fin))		
		## Si hay registros del minuto, calcular el error
		if(len(tr_real_acotado) > 0):
			calcular_diferencias(tr_real_acotado,fi_real_acotado,tr_ajustado,phi_ajustado)
		else:
			pass			
	else:
		print "Primer minuto, estima primera recta" 
		pass
	#return 

	
#***********************************************************************

def calcular_recta(tr_cr, mediana_cr):
	
	global m2
	global c2
	global alfa
	global primera_recta
	global m_ant
	global c_ant
	
	tr_cuadrados=np.array([])
	phi_cuadrados=np.array([])
		
	m,c=np.polyfit(tr_cr, mediana_cr, 1)		
	if primera_recta == True:
		m_ant=m
		c_ant=c
		m2=m
		c2=c
		primera_recta =False
	else:
		m2=(1-alfa)*m2+(alfa*m)
		c2=(1-alfa)*c2+(alfa*c)
		
		for i in range(0, len(tr_cr)):
			new_value=m2*tr_cr[i]+c2
			tr_cuadrados=np.append(tr_cuadrados,tr_cr[i])
			phi_cuadrados=np.append(phi_cuadrados, new_value)	
		m_ant=m
		c_ant=c
	return tr_cuadrados, phi_cuadrados

##**********************************************************************
	
def obtener_fi_real(_tiempo_inicio, _tiempo_fin):
	
	global t1_ref_real
	global fi_real
	global t1_ref_real_lista
	global fi_real_lista
	
	ti=_tiempo_inicio
	tf=_tiempo_fin
	t1_graf_acotado=np.array([])
	phi_real_acotado=np.array([])
	paso=len(t1_ref_real_lista)

	for i in range(0,paso):
		if ( int(t1_ref_real_lista[0]) < ti):
			t1_ref_real_lista.pop(0)
			fi_real_lista.pop(0)
		elif(int(t1_ref_real_lista[0]) >= ti and int(t1_ref_real_lista[0]) <= tf):
			t1_graf_acotado=np.append(t1_graf_acotado, t1_ref_real_lista[0])
			phi_real_acotado=np.append(phi_real_acotado, fi_real_lista[0])
			t1_ref_real_lista.pop(0)
			fi_real_lista.pop(0)			
		else:
			## No existen datos en el intervalo buscado
			break
			
	## Se asigna los valores de fi real menos el minuto extraido anteriormente	
	t1_graf_real = np.array(t1_ref_real_lista)
	fi_real=np.array(fi_real_lista)

	return t1_graf_acotado, phi_real_acotado			

##**********************************************************************

def calcular_diferencias(t_ori, phi_ori, t_cal, phi_cal):
	## Para generar de todos los valores de fi calculado y fi real, descomentar la escritura
	f=open(ruta + "TE_600.txt","a")
	t_ori_=t_ori[0]
	t_cal_=t_cal[0]

	if(t_ori_ > t_cal_):
		igualar=int(t_ori_-t_cal_) 
		for i in range(0,igualar):
			t_cal=np.delete(t_cal,(0),axis=0)
			phi_cal=np.delete(phi_cal,(0),axis=0)	
	elif(t_cal_ > t_ori_):
		sys.exit(0)

	phi_resta=np.array([])			## Para los valores de las diferencias de fi
	t1_gra_inter=np.array([])		## Referencia de tiempo para cada diferencia
	phi_interpo=np.array([])
	k=0
	alcance=0
	
	if(len(t_cal)>len(t_ori)):
		alcance=len(t_cal)
	else:
		alcance=len(t_ori)

	for i in range(0,t_cal.size):
		for j in range (k,len(t_ori)):
			if(j+1 < len(t_ori)):
				if ((t_ori[j+1] > t_cal[i]) and (t_ori[j] < t_cal[i])):
					## Interpola los puntos faltantes
					phi_aux=interpolacion(t_cal[i],t_ori[j],phi_ori[j],t_ori[j+1],phi_ori[j+1])
					resta_aux=(phi_cal[i]-phi_aux)
					phi_resta=np.append(phi_resta,resta_aux)
					t1_gra_inter=np.append(t1_gra_inter,t_cal[i])
					phi_interpo=np.append(phi_interpo,phi_aux)
					f.write("%s %s %s\n"%(t_cal[i],phi_cal[i],phi_aux))
					break
				elif(t_ori[j] == t_cal[i]):
					resta_aux=(phi_cal[i]-phi_ori[j])
					phi_resta=np.append(phi_resta,resta_aux)
					t1_gra_inter=np.append(t1_gra_inter,t_cal[i])
					phi_interpo=np.append(phi_interpo,0)
					f.write("%s %s %s\n"%(t_cal[i],phi_cal[i],phi_ori[j]))
					break
				else:
					k+=1
			else:
				if(t_ori[j] == t_cal[i]):
					resta_aux=(phi_cal[i]-phi_ori[j])
					phi_resta=np.append(phi_resta,resta_aux)
					t1_gra_inter=np.append(t1_gra_inter,t_cal[i])
					phi_interpo=np.append(phi_interpo,0)
					f.write("%s %s %s\n"%(t_cal[i],phi_cal[i],phi_ori[j]))
					pass
				else:
					pass
				break
	if len(phi_resta) <= 0:
		print("Error al calcular error %s"%(len(phi_resta)))
		sys.exit(0)
		
	f.close()

##**********************************************************************

def interpolacion(x,x1,y1,x2,y2):
	y=y1+((float(x-x1)/float(x2-x1))*(y2-y1))
	return y

##**********************************************************************

if __name__ == "__main__":
	global f
	leer_datos()
	while(1):
		procesar_datos()
