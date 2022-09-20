import copy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys

# DIJKSTRA NORMAL

def fila(ind, c):
    return ind/c

def columna(ind, c):
    return ind%c

def id(fil, col, c):
    return fil*c + col


#######################
# RELLENA DICCIONARIO #
#######################

def completaDiccionario(diccionarioEntero,clave,hijo,peso):
    
    if clave not in diccionarioEntero:   
        diccionarioEntero[clave] = {}    # SI NO HA INTRODUCIDO YA LA CLAVE, LE METE COMO VALOR UN DICCIONARIO VACIO

    diccionarioEntero[clave][hijo] = peso    # Y COMPLETA ESE DICCIONARIO VACIO, CON LA CLAVE ( HIJO ) Y EL PESO DEL EJE ( PESO ) 
    return diccionarioEntero

##########################################################
# GENERA EL LABERINTO (LOS EJES) CON LISTA DE ADYACENCIA #
##########################################################

# GRAPH, UN DICCIONARIO DE DICCIONARIOS (QUE CONTIENE LOS NODOS HIJOS CON SUS PESOS)

def creaLaberintoDiccionario(f,c,prob,semilla,semilla2):
    graph={}   
    numero = SyncRNG(seed = semilla)
    numero2 = SyncRNG(seed = semilla2)
    for i in range(f):
        for j in range(c):

            if(i>0 and numero.rand()<prob):

                # COMPLETA EL DICCIONARIO DE DICCIONARIOS

                pesoEje = numero2.randi()%12+1  # OBTIENE UN PESO RANDOM ENTRE 1 Y 12
                graph = completaDiccionario(graph,id(i, j, c),id(i-1, j, c),pesoEje)              
                graph = completaDiccionario(graph,id(i-1, j, c),id(i, j, c),pesoEje)

            if(j>0 and numero.rand()<prob):
                
                # COMPLETA EL DICCIONARIO DE DICCIONARIOS

                pesoEje = numero2.randi()%12+1  # OBTIENE UN PESO RANDOM ENTRE 1 Y 12
                graph = completaDiccionario(graph,id(i, j, c),id(i, j-1, c),pesoEje)
                graph = completaDiccionario(graph,id(i, j-1, c),id(i, j, c),pesoEje)

    return graph


#########################
# ALGORITMO DE DIJKSTRA #
#########################

def dijkstra(graph,inicio,destino):
    dist = {}
    prev = {}
    nodosSinVisitar = graph
    infinity = 999999999

    for node in nodosSinVisitar:
        dist[node] = infinity
    dist[inicio] = 0

    # MIENTRAS LA COLA NO ESTE VACIA

    while(nodosSinVisitar):
        nodoMenorDist = None

        # OBETENGO EL NODO DE MENOR DISTANCIA TENTATIA QUE ESTE EN LA COLA (nodoMenorDist)

        for node in nodosSinVisitar:
            if nodoMenorDist is None:
                nodoMenorDist = node
            elif dist[node] < dist[nodoMenorDist]:
                nodoMenorDist = node

        # OBTENGO SUS HIJOS
            
        if(nodoMenorDist == destino):
            break
        
        hijos = graph[nodoMenorDist].items()

        # PARA CADA HIJO, ACTUALIZO LA DISTANCIA TENTATIVA SI CUMPLE LA CONDICION DEL IF

        for v, peso in hijos:
            if peso + dist[nodoMenorDist] < dist[v]:
                dist[v] = peso + dist[nodoMenorDist]
                prev[v] = nodoMenorDist

        # SACO EL NODO DE MENOR DISTANCIA DE LA COLA

        nodosSinVisitar.pop(nodoMenorDist)

        # SI LLEGA AL DESTINO ACABA EL WHILE

    nodoActual = destino

    # RETORNO EL NODOACUTAL, ES DECIR DESTINO, PARA PODER HACER BACKTRACKING LUEGO, LAS DISTANCIAS TENTATIVAS Y LOS PADRES DE CADA NODO

    return dist,nodoActual,prev

###########################################################
# DEVUELVE ARRAY CON LAS HABITACIONES DEL CAMINO SOLUCION #
###########################################################

def retornaCaminoSol(inicio,nodoAct,prev):
    caminoSolucion = []
    flag = True                                 # FLAG QUE NOS DICE SI EXISTE O NO SOLUCION
    while nodoAct != inicio:                     # COMIENZA EL BACKTRACKING
        try:
            caminoSolucion.insert(0,nodoAct)     # VA INSERTANDO EN EL ARRAY, LAS HABITACIONES QUE FORMAN PARTE DE ESTE CAMINO SOLUCION
            nodoAct = prev[nodoAct]
        except KeyError:                        # SI FALLA, NO ENCUENTRA LA CLAVE QUIERE DECIR QUE NO EXISTE CAMINO ENTRE LA HABITACION DE INICIO Y LA DE DESTINO
            flag = False                        # FALSE PUESTO QUE NO TIENE SOLUCION
            break

    caminoSolucion.insert(0,inicio)             # POR ULTIMO INSERTA LA CASILLA INICIAL

    return caminoSolucion,flag


###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def listatraspasaAMatriz(mat,f,c,inicio,fin,menordist,camino_solucion,E):
    mat = np.zeros(((f*2)+1,(c*2)+1))

    # GENERA EL LABERINTO

    for i in range(0,(f)):
        for j in range(0,(c)):
            mat[i*2+1][j*2+1] = -5
            for n in range(13):
                if((i<f-1) and E.get(id(i+1,j,c)) and (id(i,j, c) in E.get(id(i+1,j,c)))):
                    mat[ i*2+2 ][ j*2+1 ] = -5
                if((j<c-1) and E.get(id(i, j+1, c)) and (id(i, j, c) in E.get(id(i, j+1, c)))):
                    mat[ i*2+1 ][ j*2+2 ] = -5
    
    # PINTA LAS HABITACIONES QUE NO SON DEL CAMINO CON SU DISTANCIA TENTATIVA

    for n in menordist:
        valor = menordist[n]
        mat[int((fila(n,c)))*2+1][int((columna(n,c)))*2+1] = valor
    
    # PINTA LOS PASILLOS DE LAS HABITACIONES QUE NO SON DEL CAMINO CON LA MENOR DE LAS DISTANCIAS TENTATIVAS

    for d in range(len(E)):
        if(d in E):
            for j in range(len(E[d])):

                # COMPARA LAS TENTATIVAS DE LAS DOS HABITACIONES Y SE QUEDA CON LA MENOR
                
                color = menorValor(menordist[d], menordist[list(E[d].keys())[j]])
                mat[int(((int((fila(d,c)))*2+1)+(int((fila(list(E[d].keys())[j],c)))*2+1))/2)][int(((int((columna(d,c)))*2+1)+(int((columna(list(E[d].keys())[j],c)))*2+1))/2)] = color
        
    # PINTA LAS HABITACIONES DEL CAMINO SOLUCION

    for k in range(len(camino_solucion)):
        mat[int((fila(camino_solucion[k],c)))*2+1][int((columna(camino_solucion[k],c)))*2+1] = 777.777

    # PINTA LOS CAMINOS DE LAS HABTACIONES DEL CAMINO SOLUCION

    for m in range(len(camino_solucion)-1):
        mat[int(((int((fila(camino_solucion[m],c)))*2+1)+(int((fila(camino_solucion[m+1],c)))*2+1))/2)][int(((int((columna(camino_solucion[m],c)))*2+1)+(int((columna(camino_solucion[m+1],c)))*2+1))/2)] = 777.777

    # PINTA LA CASILLA DE INICIO Y FIN DEL CAMINO

    mat[int((fila(inicio,c)))*2+1][int((columna(inicio,c)))*2+1] = 777.777
    mat[int((fila(fin,c)))*2+1][int((columna(fin,c)))*2+1] = 777.777

    return mat

###############################################################################
# RETORNA LA MENOR DE LAS DOS DISTANCIAS TENTATIVAS QUE RECIBE COMO PARAMETRO #
###############################################################################

def menorValor(x,y):
    if(x <= y):
        return x
    else:
        return y


############################################
#############  M  A  I  N  #################
############################################

f = int(input("Introduce el tamaño de la f: "))
c = int(input("Introduce el tamaño de la c: "))
probabilidad = float(input("Introduce la probabilidad: "))

if(probabilidad < 0 or probabilidad > 1):
    print("Introduce una probabilidad entre 0 y 1")
    probabilidad = float(input("Introduce la probabilidad: "))

# SOLICITO LAS SEMILLAS

semilla = int(input("Semilla para la generacion del laberinto: "))
semilla2 = int(input("Semilla para los pesos de los ejes: "))
semilla3 = int(input("Semilla para el inicio/fin del recorrido: "))


numero3 = SyncRNG(seed = semilla3)


print("+-+-+-+-+-+-+-+-+-+-+")
print("+ CREANDO LABERINTO +")
print("+-+-+-+-+-+-+-+-+-+-+\n")

graph = {}
matrizPintar = []

t3 = time.time() 

graph = creaLaberintoDiccionario(f,c,probabilidad,semilla,semilla2)     # RELLENA LA LISTA DE ADYACENCIA, Y EL DICCIONARIO DE DICCIONARIOS (Graph)

t2 = time.time()
t3 = t2-t3

# GENERO CON LA SEMILLA INTRODUCIDA LA HABITACION DE INICIO Y FIN DEL CAMINO

habitacionInicio = (numero3.randi() % (f*c))
habitacionFin = (numero3.randi() % (f*c))

if(habitacionFin == habitacionInicio):
    habitacionFin = (numero3.randi() % (f*c))



print("Casilla INICIO: ", habitacionInicio)
print("Casilla FIN: ", habitacionFin)
print("\n")

sys.setrecursionlimit(10**6)                                    # INCREMENTA LAS RECURSIONES POSIBLES DEL PROGRAMA

#############
# ALGORITMO #
#############

graphPinta = graph.copy()                                       # PARA QUE LO PINTE BIEN (LUEGO SE LO PASO AL METODO QUE TRANSFORMA EL GRAFO EN MATRIZ), 
                                                                # EL LABERINTO COPIO EL CONTENIDO DEL GRAPH, YA QUE EN EL DIJKSTRA LO MODIFICO
                                                                # Y SINO EL LABERINTO DE LA ZONA RECORRIDA POR DIKJSTRA NO LO PINTA BIEN

t0 = time.time()                                                # COMIENZA A CALCULAR EL TIEMPO

menor_distancia,currentNode,predecesores = dijkstra(graph,habitacionInicio,habitacionFin)  # SE LLEVA A CABO EL ALGORITMO

caminoSolucion, sepuede = retornaCaminoSol(habitacionInicio,currentNode,predecesores) # SE PUEDE CONTIENE EL FLAG ES DECIR, SI EXISTE UN CAMINO ENTRE ESOS 2 NODOS O NO
                                                                                      # CAMINOSOLUCION ES UN ARRAY CON LAS HABITACIONES DEL CAMINO
t1 = time.time()
t1 = t1-t0

costeCamino = menor_distancia[habitacionFin] 
print("Coste del camino: ",costeCamino,"\n")

for clave in menor_distancia:                                                               # RECORRO EL ARRAY DE DISTANCIAS TENTATIVAS PARA SUSTITUIR LA DISTANCIA TENTATIVA DE      
                                                                                          # LAS HABITACIONES POR DONDE EL ALGORITMO NO HA PASADO, SUSTITUYENDO EL 99999999 POR -1
    if(menor_distancia[clave] > 99999):                                                     # Y EN LA MATRIZ SE HAN DIBUJADAS DE COLOR AZUL
        menor_distancia[clave] = -1

if(sepuede == True):
    print("<---------- EXISTE CAMINO ---------->\n")
    print("Camino solucion =====> ", caminoSolucion)
    print("\nEl tiempo en generar la estructura del grafo es: ", t3, " segundos")
    print("\nEl tiempo el algoritmo DIJKSTRA NORMAL es: ",t1, " segundos")

    matrizPintar = listatraspasaAMatriz(matrizPintar,f,c,habitacionInicio,habitacionFin,menor_distancia,caminoSolucion,graphPinta)

    cmap=copy.copy(plt.get_cmap("gnuplot"))
    cmap.set_under("grey")                          # LAS CASILLAS CON VALOR INFERIOR A 0, SON PINTADAS DE COLOR AZUL
    cmap.set_bad("white")                            # EL CAMINO SE PINTA DE COLOR BLANCO  

    titulo = "DIJKSTRA \n f= "+str(f)+" c= "+str(c)+" prob= "+str(probabilidad)+" seeds= "+str(semilla)+", "+str(semilla2)+", "+str(semilla3)
    plt.title(titulo, fontdict={'fontsize':12}, pad=12)

    # DE ESTA FORMA ME PINTA EL CAMINO DE BLANCO Y SE DIFERENCIA DEL RESTO, AUNQUE EN EL VIDEO, NO ESTABA ESTO ANADIDO, POR TANTO, LAS PRUEBAS MOSTRADAS
    # SIGUEN OTRA GAMA DE COLOR, SIN EMBARGO EN LAS FOTOS DEL .ZIP SI QUE ESTA IMPLEMENTADO
    
    sb.heatmap(matrizPintar,mask=matrizPintar == 777.777,vmin=0,cmap=cmap,cbar_kws={'extend': 'min', 'extendrect': True}, annot=None, fmt="")
    plt.show()                                          # MUESTRA EL RESULTADO

else:
    print("No existe camino entre esos nodos")