import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys

# ESTE CODIGO PINTA CADA COMPONENTE CONEXA DE UN COLOR Y DE COLOR AMARILLO CON UNA ETIQUETA DONDE PONE "CO", DE COSTURA

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
        for j in range(c):                                          # V ES UNA TUPLA, QUE CONTIENE CARACTERISTICAS DE CADA HABITACION (NODO)
            V.append([id(fila(i,c)*c,columna(j,c),c),1,-1,200])      # ANADO UNA NUEVA POSICION LA 3 QUE CONTIENE "COLOR", EL VALOR QUE LE DOY A LA CASILLA PARA QUE SE PINTE EMPEZANDO POR 50
    return V

##########################
# PRIMERO EN PROFUNDIDAD #
##########################

# YA COMENTADO EN LISTA Y MATRIZ
# AUNQUE NO PRINTEO LAS ETIQUETAS CON LAS PROFUNDIDADES, LO DEJO EN EL CODIGO, AUNQUE NO "SIRVA"
def DFS(V,E,inicio,color):
    visitados =[]
    pila =[]
    pila.append(V[int(inicio)])
    V[int(inicio)][3] = color
    while pila:
        actual = pila.pop()
        if actual not in visitados:
            visitados.append(actual)
            if(V[int(inicio)][2] == -1):
                    V[int(inicio)][2] = int(actual[0])
        for i in range(len(V)):
            if V[i] not in visitados and  (([int(actual[0])]),[int(V[i][0])]) in E:
                V[i][1] = actual[1]+1
                V[i][3] = color
                V[i][2] = int(actual[0])
                pila.append(V[i])
    return visitados

######################
# PRIMERO EN ANCHURA #
######################

def BFS(V,E,inicio,color):
    visitados =[]
    cola =[]
    cola.append(V[int(inicio)])
    V[int(inicio)][3] = color
    while cola:
        actual = cola.pop(0)
        if actual not in visitados:
            visitados.append(actual)
            if(V[int(inicio)][2] == -1):
                    V[int(inicio)][2] = int(actual[0])
        
        for i in range(len(V)):
            if V[i] not in visitados and  (([int(actual[0])]),[int(V[i][0])]) in E:
                V[i][1] = actual[1]+1
                V[i][3] = color
                V[i][2] = int(actual[0])
                cola.append(V[i])
    return visitados

###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def traspasaAMatriz(mat,listaAd,visitados,f,c,V):
    mat = np.zeros(((f*2)+1,(c*2)+1))
    for i in range(0,(f)):
        for j in range(0,(c)):
            nodoActual = int(id(fila(i,c)*c,columna(j,c),c))
            mat[i*2+1][j*2+1] = 45
            if((i<f-1) and (([id(i,j,c)],[id(i+1,j,c)])) in listaAd):
                mat[ i*2+2 ][ j*2+1 ] = 0                                 # LE ASIGNA VALOR 0 A LOS CICLOS, CONVIRTIENDOLOS EN PAREDES 
            if((j<c-1) and (([id(i,j,c)],[id(i,j+1,c)])) in listaAd):
                mat[ i*2+1 ][ j*2+2 ] = 0                                 # LE ASIGNA EL VALOR 0 A LOS CICLOS   CONVIERTIENDOLOS EN PAREDES
            
            # DETECTA LAS COSTURAS

            # COLOCA POR FILAS Y POR COLUMNAS, COMPRUEBA QUE NO SE SALE DEL LIMITE ES DECIR F-1 Y C-1

            if(i<f-1):
                if(V[int(id(fila(i+1,c)*c,columna(j,c),c))][3] != V[nodoActual][3]):                # COMPRUEBA SI EL COLOR DE LAS CASILLAS ES DISTINTO SI LO ES, EN ESA PARED HAY UNA COSTURA
                    plt.text(j*2+1,i*2+2,'co',fontsize=8,color='black',verticalalignment ='center', horizontalalignment ='center')      # ANADE LA ETIQUE "CO" A LA PARED, SI SE QUITA ES MAS VISUAL
                    mat[i*2+2][j*2+1] = 1800                                                                                             # LE ASIGNA EL VALOR 350

            if(j<c-1):
                if(V[int(id(fila(i,c)*c,columna(j+1,c),c))][3] != V[nodoActual][3]):                # COMPRUEBA SI EL COLOR DE LAS CASILLAS ES DISTINTO SI LO ES, EN ESA PARED HAY UNA COSTURA
                    plt.text(j*2+2,i*2+1,'co',fontsize=8,color='black',verticalalignment ='center', horizontalalignment ='center')      # ANADE LA ETIQUE "CO" A LA PARED, SI SE QUITA ES MAS VISUAL
                    mat[i*2+1][j*2+2] = 1800                                                                                            # LE ASIGNA EL VALOR 350
                    
    for m in range(len(visitados)):

        # COMENTO LA LINEA DE LA PROFUNDIDAD PARA QUE SEA MAS VISUAL LAS COSTURAS
        #plt.text(int((columna(visitados[m][0],c)))*2+1,int((fila(visitados[m][0],c)))*2+1,visitados[m][1],fontsize=8,color='black',verticalalignment ='center', horizontalalignment ='center')
        
        # PINTA LA HABITACION CORRESPONDIENTE

        mat[int((fila(visitados[m][0],c)))*2+1][int((columna(visitados[m][0],c)))*2+1] = visitados[m][3]
        
        # EL CAMINO ES LA MEDIA ENTRE LAS 2 CASILLAS, POR TANTO PINTA EL CAMINO, VISITADOS[m][2] CONTIENE DE QUE HABITACION COLGABA VISITADOS[m][0]

        mat[int(((int((fila(visitados[m][0],c)))*2+1)+(int((fila(visitados[m][2],c)))*2+1))/2)][int(((int((columna(visitados[m][0],c)))*2+1)+(int((columna(visitados[m][2],c)))*2+1))/2)] = visitados[m][3]

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

listaAdyacencia = creaLaberintoLista(f,c,probabilidad,seed)     # CREA LA MATRIZ DE ADYACENCIA

V = rellenaNodos(f,c)                                           # RELLENA V

sys.setrecursionlimit(10**6)                                    # INCREMENTA LAS RECURSIONES POSIBLES DEL PROGRAMA


color = V[0][3]                                                 # COLOR TOMA COMO VALOR INICIAL EL QUE TIENE LOS NODOS AL INICIO, 50


##############
# ALGORITMOS #
##############

visitados = DFS(V,listaAdyacencia,V[0][0],color)
#visitados = BFS(V,listaAdyacencia,V[0][0],color)

for n in range(len(V)):
    if(V[n] not in visitados):
        color = color + 15                                  # CADA VEZ QUE SE INICIA UNA NUEVA COMPONENTE CONEXA, ES DECIR, SE HACE EL ALGORITMO EMPEZANDO
                                                           # EN UNA HABITACION NO RECORRIDA AUMENTA EN 15 EL COLOR, DE LAS COMPONENTES CONEXAS DE ESE CAMINO
        
        # VISITADOS2 CONTIENE LAS HABITACIONES QUE RECORRE EL ALGORITMO, EMPEZANDO DESDE EL RESTO DE HABITACIONES

        visitados2= DFS(V,listaAdyacencia,V[n][0],color)
        #visitados2 = BFS(V,listaAdyacencia,V[n][0],color)

        # FUSIONA EN UN UNICO ARRAY TODAS LAS HABITACIONES RECORRIDAS

        visitados.extend(visitados2)
    
matrizPintar = traspasaAMatriz(matrizPintar,listaAdyacencia,visitados,f,c,V)

t1 = time.time()
t1 = t1-t0
print("El tiempo con matriz de adyacencia es: ",t1," segundos")

# CADA COMPONENTE CONEXA DE UN COLOR, LAS PAREDES EN NEGRO, LOS CICLOS DE NARANJA Y LAS COSTURAS DE AMARILLO

plt.imshow(matrizPintar, cmap='inferno', origin='upper')

plt.colorbar()
plt.show()
