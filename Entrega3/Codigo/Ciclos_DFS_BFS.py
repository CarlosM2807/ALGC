import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys

# ESTE CODIGO CONTIENE LOS ALGORITMOS PRIMERO EN ANCHURA Y PROFUNDIDAD PARA UNA LISTA DE ADYACENCIA, ADEMAS DE LAS HABITACIONES ETIQUETADAS CON LA PROFUNDIDAD
# CORRESPONDIENTE SEGUN EL ALGORITMO APLICADO AL GRAFO, DE COLOR GRANATE EL CAMINO DEL ALGORITMO, DE NEGRO LAS PAREDES Y DE AMARILLO LOS CICLOS CON UNA ETIQUETA ROJA "CC"

# REALIZA LOS ALGORITMOS DESDE TODAS LAS HABITACIONES SIN RECORRER COMENZANDO POR LA 0, INCLUYENDO LAS ETIQUETAS DE LAS PROFUNDIDADES
# DE CADA HABITACION SEGUN DESDE DONDE EMPIECE ESE RECORRIDO Y TODOS LOS CICLOS DEL GRAFO, YA QUE LO RECORRE ENTERO

def fila(ind, c):
    return ind/c

def columna(ind, c):
    return ind%c

def id(fil, col, c):
    return fil*c + col

###############################################
# GENERA EL LABERINTO CON LISTA DE ADYACENCIA #
###############################################

def creaLaberintoLista(f,c,prob,semilla):
    E = []
    numero = SyncRNG(seed = semilla)
    for i in range (f):
        for j in range (c):
            if(i > 0 and numero.rand() < prob):
                E.append(([id(i, j, c)], [id(i-1, j, c)]))
                E.append(([id(i-1, j, c)],[id(i, j, c)]))
            if(j > 0 and numero.rand() < prob):
                E.append(([id(i, j, c)], [id(i, j-1, c)]))
                E.append(([id(i, j-1, c)], [id(i, j, c)]))
    return E

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

# YA COMENTADO EN LISTA Y MATRIZ

def DFS(V,E,inicio):
    visitados =[]
    pila =[]
    pila.append(V[int(inicio)])
    while pila:
        actual = pila.pop()
        if actual not in visitados:
            visitados.append(actual)
            if(V[int(inicio)][2] == -1):
                    V[int(inicio)][2] = int(actual[0])
        for i in range(len(V)):
            if V[i] not in visitados and  (([int(actual[0])]),[int(V[i][0])]) in E:
                V[i][1] = actual[1]+1
                V[i][2] = int(actual[0])
                pila.append(V[i])
    return visitados

######################
# PRIMERO EN ANCHURA #
######################

def BFS(V,E,inicio):
    visitados =[]
    cola =[]
    cola.append(V[int(inicio)])
    while cola:
        actual = cola.pop(0)
        if actual not in visitados:
            visitados.append(actual)
            if(V[int(inicio)][2] == -1):
                    V[int(inicio)][2] = int(actual[0])
        for i in range(len(V)):
            if V[i] not in visitados and  (([int(actual[0])]),[int(V[i][0])]) in E:
                V[i][1] = actual[1]+1
                V[i][2] = int(actual[0])
                cola.append(V[i])
    return visitados

#####################################
# COLOCA UNA ETIQUETA EN LOS CICLOS #
#####################################

def detectaCiclo(f,c,matrizPintar):
    for i in range(0,f):
        for j in range(0,c):
            if(matrizPintar[ i*2+2 ][ j*2+1 ] == 45):   # SI ES UN CICLO TIENE EL VALOR 45

                # ANADE LA ETIQUETA CC QUE CORRESPONDE A UN CICLO EN LA CASILLA ADECUADA

                plt.text(j*2+1,i*2+2,'cc',fontsize=8,color='red',verticalalignment ='center', horizontalalignment ='center')
            
            if(matrizPintar[ i*2+1 ][ j*2+2 ] == 45):
                
                # ANADE LA ETIQUETA CC QUE CORRESPONDE A UN CICLO EN LA CASILLA ADECUADA

                plt.text(j*2+2,i*2+1,'cc',fontsize=8,color='red',verticalalignment ='center', horizontalalignment ='center')
    
    return matrizPintar

###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def traspasaAMatriz(mat,listaAd,visitados,f,c):
    mat = np.zeros(((f*2)+1,(c*2)+1))
    for i in range(0,(f)):
        for j in range(0,(c)):
            mat[i*2+1][j*2+1] = 45
            if((i<f-1) and (([id(i,j,c)],[id(i+1,j,c)])) in listaAd):
                mat[ i*2+2 ][ j*2+1 ] = 45                              # LE ASIGNA EL VALOR 45 A LOS CICLOS
            if((j<c-1) and (([id(i,j,c)],[id(i,j+1,c)])) in listaAd):
                mat[ i*2+1 ][ j*2+2 ] = 45                              # LE ASIGNA EL VALOR 45 A LOS CICLOS

    for m in range(len(visitados)):

         # AÑADE LA ETIQUETA DE LA PROFUNDIDAD A LA HABITACION

        plt.text(int((columna(visitados[m][0],c)))*2+1,int((fila(visitados[m][0],c)))*2+1,visitados[m][1],fontsize=7,color='white',verticalalignment ='center', horizontalalignment ='center')
        
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

print("+-+-+-+-+-+-+-+-+-+-+")
print("+ CREANDO LABERINTO +")
print("+-+-+-+-+-+-+-+-+-+-+")

V = []
matrizPintar = []
listaAdyacencia = []

t0 = time.time()                                                # COMIENZA A CALCULAR EL TIEMPO

listaAdyacencia = creaLaberintoLista(f,c,probabilidad,seed)     # CREA LA LISTA DE ADYACENCIA

V = rellenaNodos(f,c)                                           # RELLENA V

sys.setrecursionlimit(10**6)                                    # INCREMENTA LAS RECURSIONES POSIBLES DEL PROGRAMA

##############
# ALGORITMOS #
##############

visitados = DFS(V,listaAdyacencia,V[0][0])
#visitados = BFS(V,listaAdyacencia,V[0][0])

# REALIZA EL ALGORITMO CON TODAS LAS HABITACIONES QUE NO HAN SIDO RECORRIDAS

for n in range(len(V)):
    if(V[n] not in visitados):

        # VISITADOS2 CONTIENE LAS HABITACIONES QUE RECORRE EL ALGORITMO, EMPEZANDO DESDE EL RESTO DE HABITACIONES
        
        visitados2= DFS(V,listaAdyacencia,V[n][0])
        #visitados2= BFS(V,listaAdyacencia,V[n][0])

        # FUSIONA EN UN UNICO ARRAY TODAS LAS HABITACIONES RECORRIDAS

        visitados.extend(visitados2)

matrizPintar = traspasaAMatriz(matrizPintar,listaAdyacencia,visitados,f,c)
matrizPintar = detectaCiclo(f,c,matrizPintar)

t1 = time.time()
t1 = t1-t0
print("El tiempo con matriz de adyacencia es: ",t1," segundos")

# DE GRANATE EL RECORRIDO, DE NEGRO LAS PAREDES Y DE AMARILLO LOS CICLOS, CON UNA ETIQUETA ROJA "CC"

plt.imshow(matrizPintar, cmap='inferno', origin='upper')

plt.colorbar()
plt.show()
