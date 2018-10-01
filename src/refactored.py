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




from sic_config import Configuration, FileReader
from phi_calculator import PhiCalculator
from sic_collections import CircularList



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
global fi_metodo3_todos
global rtt_todos
global t1_todos
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

def leer_datos(): 

	global fi_metodo3_todos
	global rtt_todos
	global t1_todos
	global tiempo_i
	global corte_proceso
	global t1_ref_real_lista
	global fi_real_lista
	
	phi_calculator = PhiCalculator()
	file_reader = FileReader(Configuration('configuracion.cfg'), phi_calculator)

	corte_proceso=0

	## Inicio de lectura DATOS
	tiempo_i=datetime.now()
	print ("Tiempo inicial de calculo: %s"%(tiempo_i)) 

	rtt_todos = file_reader.get_rtt_values()
	fi_metodo3_todos = file_reader.get_phi_values()
	t1_todos = file_reader.get_t1_values()

	## Inicio de lectura datos para los valores de T1_PPS 
	print "Inicio lectura de t1_pps: \t%s" % datetime.now()
	t1Pps_new = file_reader.get_t1_pps_values()

	## Inicio de lectura datos para los valores de T2_PPS 
	print "Inicio lectura de t2_pps: \t%s" % datetime.now()
	t2Pps_new = file_reader.get_t2_pps_values()

	# Verificacion de secuencia de tiempos en datos de pps
	print "Verificacion de secuencia en datos pps: \t%s" % datetime.now()
	t1_ref_real_lista, fi_real_lista = phi_calculator.pair_and_verify(t1Pps_new, t2Pps_new)

	print "Fin de lectura y ajuste de tiempos: \t%s" % datetime.now()

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
	
	tamanio_mediana=120						## Tamaño de la lista circular (10 minutos)
	tiempo_calculo=61 						## Ventanas de medicion (1 minuto)
	mediana_temporal=0
	rtt_temporal=0
	ventana_rtt=60							## Ventana de rtt para obtener el minimo

	buffer_mediana=CircularList(tamanio_mediana)
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
		print "{} / {}".format(i, len(fi_metodo3_todos))		
		valor_phi_estimado=fi_metodo3_todos[i]
		## Condicion para llenar la lista circular
		if completo_mediana == False:									
			buffer_mediana.append(valor_phi_estimado)
			## Agregado para almacenar el rtt
			#------------------------------------------------------------
			if (tamanio_mediana-len(buffer_mediana) < ventana_rtt):
				valor_rtt=rtt_todos[i]
				rtt_minimo=np.append(rtt_minimo,valor_rtt)
			#------------------------------------------------------------
			if (len(buffer_mediana) == tamanio_mediana):		
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
					mediana = buffer_mediana.median()					
					buffer_minuto_medianas=np.append(buffer_minuto_medianas,mediana)				## Agrega al array de medianas
					buffer_minuto_tiempos=np.append(buffer_minuto_tiempos,tiempo_actual)			## Agrega el tiempo de referencia
					mediana_temporal=mediana							## Mantiene el valor en memoria
					contador_segundos+=1								## Incrementa la secuencia de segundos
					#****************************************
					#g.write("%s %s 260000\n"%(i,tiempo_actual))
					#****************************************
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
							#f.write("%s %s %s 1\n"%(buffer_minuto_tiempos[buffer_minuto_tiempos.size-1],corte_proceso,ultimo_rtt_minimo))
							#f.write("%s %s %s 1\n"%(buffer_minuto_tiempos[0],corte_proceso,ultimo_rtt_minimo))
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
						#if (mediana_temporal == 0):
							#print "1- %s Aqui la mediana le asigna 0" %(i)
							#tem_mediana=np.asarray(buffer_mediana)				## Convierte la lista en np.array para obtener la mediana
							#mediana=np.median(tem_mediana)
						#*****************************************			
						buffer_colector_medianas=np.append(buffer_minuto_medianas,mediana_temporal)
						buffer_colector_tiempos=np.append(buffer_minuto_tiempos,tiempo_siguiente+x)
						# Esto porque justo coincide en el cambio
						#if rtt_temporal == 0:
							#rtt_temporal=rtt_todos[i]
							#print "Aqui vale 0 y agregamos %s %s"%(rtt_temporal,tiempo_siguiente+x)
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
					mediana = buffer_mediana.median()					
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
					mediana=buffer_mediana.median()					
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
					mediana=buffer_mediana.median()	
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

	return t1_graf_acotado, phi_real_acotado			

##**********************************************************************

def calcular_diferencias(t_ori, phi_ori, t_cal, phi_cal):
	## Para generar de todos los valores de fi calculado y fi real, descomentar la escritura
	f=open(ruta + "TE_120.txt","a")
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
