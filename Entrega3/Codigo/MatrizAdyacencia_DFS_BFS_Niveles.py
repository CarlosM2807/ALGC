import matplotlib.pyplot as plt
import numpy as np
import random
from numpy.core.arrayprint import printoptions
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys


# ESTE CODIGO CONTIENE LOS ALGORITMOS PRIMERO EN ANCHURA Y PROFUNDIDAD PARA UNA MATRIZ DE ADYACENCIA, ADEMAS DE LAS HABITACIONES ETIQUETADAS CON LA PROFUNDIDAD
# CORRESPONDIENTE SEGUN EL ALGORITMO APLICADO AL GRAFO, DE COLOR AMARILLO EL CAMINO DEL ALGORITMO Y DE ROJO POR DONDE NO PASA, DE NEGRO LAS PAREDES

def fila(id,c):
    return id / c 

def columna(id,c):
    return id % c

def id(fil,col,c):
    return fil*c + col

###############################################
# GENERA EL LABERINTO CON LISTA DE ADYACENCIA #
###############################################

def creaLaberintoMatriz(f,c,prob,semilla):
    matrizAd = np.zeros((((f*c)),((f*c))))
    numero = SyncRNG(seed = semilla)
    for i in range (0,f):
        for j in range (0,c):
            if(i > 0 and numero.rand() < prob):
                matrizAd[id(i, j, c)][id(i-1, j, c)] = 1
                matrizAd[id(i-1, j, c)][id(i, j, c)] = 1
            if(j > 0 and numero.rand() < prob):
                matrizAd[id(i, j, c)][id(i, j-1, c)] = 1
                matrizAd[id(i, j-1, c)][id(i, j, c)] = 1
    return matrizAd

#############
# RELLENA V #
#############

def rellenaNodos(f,c):
    V = []
    for i in range(f):
        for j in range(c):                                      # V ES UNA TUPLA, QUE CONTIENE CARACTERISTICAS DE CADA HABITACION (NODO)
            V.append([id(fila(i,c)*c,columna(j,c),c),1,-1])     # LA POSICION 0 TIENE EL Nº DE LA HABITACION, LA 1 LA PROFUNDIDAD DE LA HABITACION EN LA BUSQUEDA, Y LA 2 CONTIENE EL NODO DE DONDE "CUELGA"
    return V
      
##########################
# PRIMERO EN PROFUNDIDAD #
##########################

def DFS(V,E,inicio):
    visitados =[]                                               # ALMACENA LAS HABITACIONES QUE HAN SIDO RECORRIDAS POR EL ALGORITMO
    pila =[]                                                    # ACTUA COMO UNA PILA
    pila.append(V[inicio])                                      # COLOCA EL VERTICE DE ORIGEN EN UNA PILA 
    while(pila):
        actual = pila.pop()                                     # DESAPILA EL VERTICE, Y AHORA ES EL ACTUAL
        if(actual not in visitados):                            # SI ESTE NO HA SIDO VISITADO
            visitados.append(actual)                            # LO ANADE EN VISITADOS
            if(V[inicio][2] == -1):                             # EL NODO INICIAL VIENE DE SI MISMO ENTONCES SE AÑADE A LA PROPIEDAD NODO DE DONDE CUELGA
                    V[inicio][2] = int(actual[0])
        for i in range(len(V)):                                 # RECORRE EL ARRAY DE NODOS
            if(V[i] not in visitados and  E[int(actual[0])][int(V[i][0])] == 1):    # SI NO ESTA EN VISITADOS, Y VALE 1 EN E, ES DECIR ESTAN CONECTADOS(ARRAY DE EJES)
                V[i][1] = actual[1]+1                           # AUMENTA LA PROFUNDIDAD, (ETIQUETA DE LA HABITACION)
                V[i][2] = int(actual[0])                        # SE ACTUALIZA EL NODO DEL QUE CUELGA
                pila.append(V[i])                               # AÑADE A LA PILA PARA SEGUIR CON EL ALGORITMO
    return visitados                                            # RETORNA UN ARRAY QUE CONTIENE TODAS LAS HABITACIONES RECORRIDAS POR EL ALGORITMO

######################
# PRIMERO EN ANCHURA #
######################

def BFS(V,E,inicio):
    visitados = []
    cola = []
    cola.append(V[inicio])
    while(cola):
        actual = cola.pop(0)                                    # IGUAL QUE PROFUNDIDAD, PERO AHORA UTILIZANDO UNA COLA
        if(actual not in visitados):
            visitados.append(actual)
            if(V[inicio][2] == -1):
                    V[inicio][2] = int(actual[0])
        for i in range(len(V)):
            if(V[i] not in visitados and E[int(actual[0])][int(V[i][0])] == 1):
                V[i][1] = actual[1]+1                           # TAMBIEN AUMENTA LA PROFUNDIDAD 
                V[i][2] = int(actual[0])
                cola.append(V[i])
    return visitados                                            # RETORNA UN ARRAY QUE CONTIENE TODAS LAS HABITACIONES RECORRIDAS POR EL ALGORITMO


###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def traspasaAMatriz(mat,matrizAd,visitados,f,c):
    mat = np.zeros(((f*2+1),(c*2+1)))
    for i in range(0,f):
        for j in range(0,c):
            mat[i*2+1][j*2+1] = 10
            if((i<f-1) and matrizAd[id(i,j,c)][id(i+1,j,c)] == 1):
                mat[ i*2+2 ][ j*2+1 ] = 10
            if((j<c-1) and matrizAd[id(i,j,c)][id(i,j+1,c)] == 1):
                mat[ i*2+1 ][ j*2+2 ] = 10

    for m in range(len(visitados)):

        # AÑADE LA ETIQUETA DE LA PROFUNDIDAD A LA HABITACION
        
        plt.text(int((columna(visitados[m][0],c)))*2+1,int((fila(visitados[m][0],c)))*2+1,visitados[m][1],fontsize=8,color='black',verticalalignment ='center', horizontalalignment ='center')
        
        # PINTA LA HABITACION CORRESPONDIENTE

        mat[int((fila(visitados[m][0],c)))*2+1][int((columna(visitados[m][0],c)))*2+1] = 20
        
        # EL CAMINO ES LA MEDIA ENTRE LAS 2 CASILLAS, POR TANTO PINTA EL CAMINO, VISITADOS[m][2] CONTIENE DE QUE HABITACION COLGABA VISITADOS[m][0]

        mat[int(((int((fila(visitados[m][0],c)))*2+1)+(int((fila(visitados[m][2],c)))*2+1))/2)][int(((int((columna(visitados[m][0],c)))*2+1)+(int((columna(visitados[m][2],c)))*2+1))/2)] = 20

    return mat

############################################
#############  M  A  I  N  #################
############################################

f = int(input("Introduce el tamaño de la f: "))
c = int(input("Introduce el tamaño de la c: "))
probabilidad = float(input("Introduce la probabilidad: "))

if(probabilidad < 0 or probabilidad > 1):
    print("Introduce una probabilidad entre 0 y 1")
    probabilidad = float(input("Introduce la probabilidad: "))

seed = int(input("Introduce el valor de la semilla: "))

#PIDE LA HABITACION POR LA QUE EMPIEZA A HACER EL RECORRIDO

habitacionInicio = int(input("Habitacion por donde empieza el algorimo siguiendo nombrado del ejemplo Lab 3.1: "))

print("+-+-+-+-+-+-+-+-+-+-+")
print("+ CREANDO LABERINTO +")
print("+-+-+-+-+-+-+-+-+-+-+")

V = [[]]
matrizPintar = []
matrizAdyacencia = []

matrizAdyacencia = creaLaberintoMatriz(f,c,probabilidad,seed)   # CREA LA MATRIZ DE ADYACENCIA

V = rellenaNodos(f,c)                                           # RELLENA V

sys.setrecursionlimit(10**6)                                    # INCREMENTA LAS RECURSIONES POSIBLES DEL PROGRAMA

##############
# ALGORITMOS #
##############

t0 = time.time()                                                # COMIENZA A CALCULAR EL TIEMPO

visitados = DFS(V,matrizAdyacencia,habitacionInicio)
#visitados = BFS(V,matrizAdyacencia,habitacionInicio)

t1 = time.time()
t1 = t1-t0

matrizPintar = traspasaAMatriz(matrizPintar,matrizAdyacencia,visitados,f,c)

print("El tiempo con matriz de adyacencia es: ",t1, " segundos")

# DE AMARILLO EL RECORRIDO Y DE NEGRO LAS PAREDES  

plt.imshow(matrizPintar, cmap='inferno',origin='upper')

plt.colorbar()
plt.show()