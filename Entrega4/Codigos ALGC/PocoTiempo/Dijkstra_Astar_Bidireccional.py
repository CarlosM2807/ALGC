import copy
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import time
from SyncRNG import SyncRNG
import sys
import queue


# BIDIRECCIONALES

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

        diccionarioEntero[clave] = {}                       # A CADA CLAVE QUE NO ESTE YA EN EL DICCIONARIO LE METE UN DICCIONARIO VACIO

    diccionarioEntero[clave][hijo] = peso                   # INTRODUCE EL PESO

    return diccionarioEntero

##########################################################
# GENERA EL LABERINTO (LOS EJES) CON LISTA DE ADYACENCIA #
##########################################################

# GRAPH, UN DICCIONARIO DE DICCIONARIOS (QUE CONTIENE LOS NODOS HIJOS CON SUS PESOS)

def creaLaberintoLista(f,c,prob,semilla,semilla2):
    graph={}

    numero = SyncRNG(seed = semilla)
    numero2 = SyncRNG(seed = semilla2)

    for i in range(f):
        for j in range(c):
            if(i>0 and numero.rand()<prob):

                pesoEje = numero2.randi()%12+1                                         # GENERA UN PESO RANDOM ENTRE 1-12

                graph = completaDiccionario(graph,id(i, j, c),id(i-1, j, c),pesoEje)   # LLAMO AL METODO QUE COMPLETA EL DICCIONARIO
                                                                                       # LE PASO EL NODO CON EL QUE CONECTA Y SU PESO
                graph = completaDiccionario(graph,id(i-1, j, c),id(i, j, c),pesoEje)
            if(j>0 and numero.rand()<prob):

                pesoEje = numero2.randi()%12+1                                         # GENERA UN PESO RANDOM ENTRE 1-12

                graph = completaDiccionario(graph,id(i, j, c),id(i, j-1, c),pesoEje)   # LLAMO AL METODO QUE COMPLETA EL DICCIONARIO
                                                                                       # LE PASO EL NODO CON EL QUE CONECTA Y SU PESO
                graph = completaDiccionario(graph,id(i, j-1, c),id(i, j, c),pesoEje)
    return graph


######################################
# ALGORITMO DE DIJKSTRA BIDIRECIONAL #
######################################

def dijkstra(graph,inicio,destino):
    dist = {}
    prev = {}
    cola = queue.PriorityQueue()  # CREAMOS LA COLA DE PRIORIDAD 1 (LA ENCARGADA DE IR DEL INICIO A LA CASILLA DE CORTE)
    casillaCorte = None
    dist2 = {}                    # MISMAS ESTRUCTURAS QUE PARA UNA COLA
    prev2 = {}
    cola2 = queue.PriorityQueue() # CREAMOS LA COLA DE PRIORIDAD 1 (LA ENCARGADA DE IR DEL INICIO A LA CASILLA DE CORTE)

    infinity = 999999999
    dist[inicio] = 0
    dist2[destino] = 0

    recorridos = {}                # SIRVE PARA ALMACENAR LAS CASILLAS QUE RECORRE LA COLA 1 

    for vertex in graph:
                                  # RELLENO EL DICCIONARIO DE DISTANCIAS TENTATIVAS Y EL DICCIONARIO DE PREDECESORES
        if(vertex != inicio):
            dist[vertex] = infinity
            prev[vertex] = None
        if(vertex != destino):
            dist2[vertex] = infinity
            prev2[vertex] = None

        cola.put((infinity,vertex))          # RELLENO LA COLA DE PRIORIDAD 1
        cola2.put((infinity,vertex))         # RELLENO LA COLA DE PRIORIDAD 2

    cola.put((0,inicio))                     # PRIORIDAD 0 AL NODO INICIAL DE LA COLA 1 ---> INICIO
    cola2.put((0,destino))                   # PRIORIDAD 0 AL NODO INICIAL DE LA COLA 2 ---> DESTINO

    
    # MIENTRAS LA COLA1 Y LA COLA2 NO ESTE VACIA

    while(cola and cola2):

        # EN ESTE CASO EL MAS ARRIBA DE LAS COLAS DE PRIORIDAD, SON LOS NODOS CON MENOR DISTANCIA TENTATIVA
        # SE OBTIENE CON .GET() PUESTO QUE ESTAN ORDENADOS DE MENOR A MAYOR PRIORIDAD --> DISTANCIA TENTATIVA

        u = cola.get()
        u2 = cola2.get()

        # OBTENGO SUS HIJOS, PARA CADA UNA DE LOS NODOS CON MENOR DISTANCIA TENTATIVA

        hijos = graph[u[1]].items()
        hijos2 = graph[u2[1]].items()

        # EN EL DICCIONARIO DE RECORRIDOS, ALMACENOS LOS NODOS RECORRIDOS POR LA COLA, COMO CLAVE EL NODO Y COMO VALOR 0 

        recorridos[u[1]] = 0

        # COMPRUEBO SI EL NODO QUE SACO DE LA COLA2 ESTA ENTRE LAS CLAVE DEL DICCIONARIO RECORRIDO
        # SI ESTA, SIGNIFICA QUE EN ESE NODO AMBAS BUSQUEDAS SE ENCEUNTRAN POR PRIMERA VEZ, Y ESA VA A SER LA CASILLA DE CORTE
        # NO ESTA, CONTINUA, PUESTO QUE TODAVIA NO SE HAN ENCONTRADO AMBAS BUSQUEDAS

        if(u2[1] in recorridos.keys()):
            casillaCorte = u2[1]
            break

        # PARA CADA HIJO, ACTUALIZO LA DISTANCIA TENTATIVA SI CUMPLE LA CONDICION DEL IF, AHORA CON 2 COLAS
        
        for v,peso in hijos:
            if peso+dist[u[1]] < dist[v]:
                dist[v] = peso + dist[u[1]]
                prev[v] = u[1]
                cola.put((dist[u[1]]+peso,v))

        for v,peso in hijos2:
            if peso+dist2[u2[1]] < dist2[v]:
                dist2[v] = peso + dist2[u2[1]]
                prev2[v] = u2[1]
                cola2.put((dist2[u2[1]]+peso,v))

        # SI LLEGA AL DESTINO PARA LA COLA1 O AL INICIO PARA COLA2 ACABA EL WHILE
        
        if(u[1] == destino):
            break
        if(u2[1] == inicio):
            break

    # RETORNO EL NODOACUTAL, ES DECIR DESTINO, PARA PODER HACER BACKTRACKING LUEGO, LAS DISTANCIAS TENTATIVAS Y LOS PADRES DE CADA NODO
    
    return dist,prev,dist2,prev2,casillaCorte

def astar(graph,inicio,destino):
    dist = {}
    prev = {}
    cola = queue.PriorityQueue()  # CREAMOS LA COLA DE PRIORIDAD

    dist2 = {}
    prev2 = {}
    cola2 = queue.PriorityQueue()
    
    casillaCorte = None

    infinity = 999999999
    dist[inicio] = 0
    dist2[destino] = 0
    recorridos = {}

    for vertex in graph:
        if(vertex != inicio):
            dist[vertex] = infinity
            prev[vertex] = None
        if(vertex != destino):
            dist2[vertex] = infinity
            prev2[vertex] = None
        cola.put((infinity,vertex))          # RELLENO LA COLA DE PRIORIDAD
        cola2.put((infinity,vertex))
    cola.put((0,inicio))                     # PRIORIDAD 0 AL NODO INCIAL
    cola2.put((0,destino))
    
    # MIENTRAS LA COLA NO ESTE VACIA

    while(not cola.empty() and not cola2.empty()):

        # OBTENGO EL NODO DE MENOR DISTANCIA TENTATIVA QUE ESTE EN LA COLA (nodoMenorDist)
        # EN ESTE CASO EL MAS ARRIBA DE LA COLA DE PRIORIDAD

        u = cola.get()
        u2 = cola2.get()

        # OBTENGO SUS HIJOS

        hijos = graph[u[1]].items()
        hijos2 = graph[u2[1]].items()

        recorridos[u[1]] = 0

        if(u2[1] in recorridos.keys()):
            casillaCorte = u2[1]
            break

        # PARA CADA HIJO, ACTUALIZO LA DISTANCIA TENTATIVA SI CUMPLE LA CONDICION DEL IF
        

        for v,peso in hijos:
            if peso+dist[u[1]] < dist[v]:
                dist[v] = peso + dist[u[1]]
                prev[v] = u[1]
                cola.put((dist[u[1]]+distManhattan(u[1],destino),v))

        for v,peso in hijos2:
            if peso+dist2[u2[1]] < dist2[v]:
                dist2[v] = peso + dist2[u2[1]]
                prev2[v] = u2[1]
                cola2.put((dist2[u2[1]]+distManhattan(u2[1],inicio),v))

        # SI LLEGA AL DESTINO ACABA EL WHILE
        
        if(u[1] == destino):
            break
        if(u2[1] == inicio):
            break

    # RETORNO LOS DICCIONARIOS DE DISTNACIAS TENTATIVAS Y PREDECESORES DE AMBAS COLAS, Y LA CASILLA DONDE AMBAS BUSQUEDAS SE ENCUENTRAN

    return dist,prev,dist2,prev2,casillaCorte


######################################################
# HALLA LA DISTANCIA DE MANHATTAN (NUEVA HEURISTICA) #
######################################################

def distManhattan(nodo, destino):

    nodox = int((fila(nodo,c)))                      # OBTIENE LA COORDENADA X DE ESA HABITACION EN LA MATRIZ
    nodoy = int((columna(nodo,c)))                   # OBTIENE LA COORDENADA Y DE ESA HABITACION EN LA MATRIZ

    destinox = int((fila(destino,c)))                # OBTIENE LA COORDENADA X DE ESA HABITACION EN LA MATRIZ
    destinoy = int((columna(destino,c)))             # OBTIENE LA COORDENADA Y DE ESA HABITACION EN LA MATRIZ

    return (abs(nodox-destinox) + abs(nodoy-destinoy))   # LA DISTANCIA DE MANHATTAN

###########################################################
# DEVUELVE ARRAY CON LAS HABITACIONES DEL CAMINO SOLUCION #
###########################################################

def retornaCaminoSol(inicio,corte,prev):
    caminoSolucion = []
    flag = True                                 # FLAG QUE NOS DICE SI EXISTE O NO SOLUCION
    while corte != inicio:                     # COMIENZA EL BACKTRACKING
        try:
            caminoSolucion.insert(0,corte)     # VA INSERTANDO EN EL ARRAY, LAS HABITACIONES QUE FORMAN PARTE DE ESTE CAMINO SOLUCION
            corte = prev[corte]
        except KeyError:                        # SI FALLA, NO ENCUENTRA LA CLAVE QUIERE DECIR QUE NO EXISTE CAMINO ENTRE LA HABITACION DE INICIO Y LA DE DESTINO
            flag = False                        # FALSE PUESTO QUE NO TIENE SOLUCION
            break
    caminoSolucion.insert(0,inicio)             # POR ULTIMO INSERTA LA CASILLA INICIAL
    
    return caminoSolucion,flag

###################################
# CONVIERTE EL GRAFO A UNA MATRIZ #
###################################

def listatraspasaAMatriz(mat,f,c,inicio,fin,camino_solucion,E,menordist,menordist2,sep):
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
    
    # PINTA LAS HABITACIONES QUE NO SON DEL CAMINO CON SU DISTANCIA TENTATIVA, SI ES -1 AZUL

    for n in menordist:
        color = menordist[n]
        mat[int((fila(n,c)))*2+1][int((columna(n,c)))*2+1] = color
    
    # PINTA LOS PASILLOS DE LAS HABITACIONES QUE NO SON DEL CAMINO CON LA MENOR DE LAS DISTANCIAS TENTATIVAS

    for d in range(len(E)):
        if(d in E):
            for j in range(len(E[d])):

                # COMPARA LAS TENTATIVAS DE LAS DOS HABITACIONES Y SE QUEDA CON LA MENOR  

                color = menorValor(menordist[d], menordist[list(E[d].keys())[j]])
                mat[int(((int((fila(d,c)))*2+1)+(int((fila(list(E[d].keys())[j],c)))*2+1))/2)][int(((int((columna(d,c)))*2+1)+(int((columna(list(E[d].keys())[j],c)))*2+1))/2)] = color


    # PINTA LAS HABITACIONES QUE NO SON DEL CAMINO CON SU DISTANCIA TENTATIVA
    # COMO EL PRIMER DICCIONARIO DE DISTANCIAS TENTATIVAS YA PINTA TODAS LAS HABITACIONES Y PASILLOS QUE NO HAN SIDO RECORRIDOS DE AZUL, AHORA CUANDO EL VALOR SEA -1
    # PASS ES DECIR, NO PINTAMOS NADA, SINO NO PINTARIA LAS DOS MANCHAS DE CASILLAS RECORRIDAS

    for n in menordist2:
        color = menordist2[n]
        if(color == -1):
            pass
        else:
            mat[int((fila(n,c)))*2+1][int((columna(n,c)))*2+1] = color
    
    # PINTA LOS PASILLOS DE LAS HABITACIONES QUE NO SON DEL CAMINO CON LA MENOR DE LAS DISTANCIAS TENTATIVAS

    for d in range(len(E)):
        if(d in E):
            for j in range(len(E[d])):

                # COMPARA LAS TENTATIVAS DE LAS DOS HABITACIONES Y SE QUEDA CON LA MENOR
                
                color = menorValor(menordist2[d], menordist2[list(E[d].keys())[j]])
                if(color == -1):
                    pass
                else:
                    mat[int(((int((fila(d,c)))*2+1)+(int((fila(list(E[d].keys())[j],c)))*2+1))/2)][int(((int((columna(d,c)))*2+1)+(int((columna(list(E[d].keys())[j],c)))*2+1))/2)] = color

    # PINTA LAS HABITACIONES DEL CAMINO SOLUCION, ASIGNO EL VALOR 777.777 
    # PARA QUE POSTERIORMENTE CON LA MASCARA EL CAMINO SEA PINTADO DE BLANCO Y SE DISTINGA MEJOR

    for k in range(len(camino_solucion)):
        mat[int((fila(camino_solucion[k],c)))*2+1][int((columna(camino_solucion[k],c)))*2+1] = 777.777

    # PINTA LOS CAMINOS DE LAS HABTACIONES DEL CAMINO SOLUCION
   
    for m in range(len(camino_solucion)-1):
        if(m == sep):
            pass
        else:
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

eleccion = int(input("INTRODUCE --------> 0 PARA DIJKSTRA // 1 PARA A* :"))

numero3 = SyncRNG(seed = semilla3)


print("+-+-+-+-+-+-+-+-+-+-+")
print("+ CREANDO LABERINTO +")
print("+-+-+-+-+-+-+-+-+-+-+\n")

graph = {}
matrizPintar = []

t3 = time.time() 

graph = creaLaberintoLista(f,c,probabilidad,semilla,semilla2)     # RELLENA LA LISTA DE ADYACENCIA, Y EL DICCIONARIO DE DICCIONARIOS (Graph)

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

##############
# ALGORITMOS #
##############

t0 = time.time()                                                # COMIENZA A CALCULAR EL TIEMPO

# HACE DIJKSTRA O A* DEPENDIENDO DE LO INTRODUCIDO

if(eleccion == 0):
    menor_distancia,predecesores,menor_distancia2,predecesores2,casillaCorte = dijkstra(graph,habitacionInicio,habitacionFin)   # SE LLEVA A CABO EL ALGORITMO
if(eleccion == 1):
    menor_distancia,predecesores,menor_distancia2,predecesores2,casillaCorte = astar(graph,habitacionInicio,habitacionFin)   # SE LLEVA A CABO EL ALGORITMO


t1 = time.time()
t1 = t1-t0

caminoSolucion,sepuede = retornaCaminoSol(habitacionInicio,casillaCorte,predecesores)     # OBTIENE EL CAMINO SOLUCION DE LA CASILLA DE INICIO A LA DE CORTE

sep = len(caminoSolucion)-1                                                               # HALLA LA POSICION DEL NODO DE UNION DE LOS DOS CAMINOS

caminoSolucion2,sepuede2 = retornaCaminoSol(habitacionFin,casillaCorte,predecesores2)      # OBTIENE EL CAMINO SOLUCION DE LA DE CORTE A LA DE DESTINO

caminoSolucion.extend(caminoSolucion2)                                                     # FUSIONA LOS DOS CAMINOS EN UNO



for clave in menor_distancia:                    # RECORRO EL ARRAY DE DISTANCIAS TENTATIVAS PARA SUSTITUIR LA DISTANCIA TENTATIVA DE                                                 
                                                 # LAS HABITACIONES POR DONDE EL ALGORITMO NO HA PASADO, SUSTITUYENDO EL 99999999 POR -1
    if(menor_distancia[clave] > 99999):          # Y EN LA MATRIZ SE HAN DIBUJADAS DE COLOR AZUL
        menor_distancia[clave] = -1

for clave in menor_distancia2:
    if(menor_distancia2[clave] > 99999):
        menor_distancia2[clave] = -1

# PARA QUE HAYA CAMINO, LAS DOS COLAS HAN TENIDO QUE LLEGAR A SU "OBJETIVO", HACIENDO EL BACKTRACKING, POR ELLO AMBOS FLAGS A TRUE
# Y ADEMAS AMBAS BUSQUEDAS SE TIENEN QUE ENCONTRAR, POR TANTO LA CASILLA DE CORTE TIENE QUE SER DISTINTO A NONE

if(sepuede == True  and sepuede2 == True and casillaCorte != None):
    print("<---------- EXISTE CAMINO ---------->\n")
    print("Camino solucion =====> ", caminoSolucion)
    print("\nEl tiempo en generar la estructura del grafo es: ", t3, " segundos")
    if(eleccion == 0):
        print("\nEl tiempo del algoritmo DIJKSTRA BUSQUEDA BIDIRECCIONAL es: ",t1, " segundos")
    if(eleccion == 1):
        print("\nEl tiempo del algoritmo A* BUSQUEDA BIDIRECCIONAL es: ",t1, " segundos")

                                                                                                                            #copia
    matrizPintar = listatraspasaAMatriz(matrizPintar,f,c,habitacionInicio,habitacionFin,caminoSolucion,graph,menor_distancia,menor_distancia2,sep)

    cmap=copy.copy(plt.get_cmap("gnuplot"))
    cmap.set_under("grey")                          # LAS CASILLAS CON VALOR INFERIOR A 0, SON PINTADAS DE COLOR AZUL
    cmap.set_bad("white")        # EL CAMINO SE PINTA DE COLOR BLANCO                   

    # PONE UN TITULO CON LOS PARAMETROS INTRODUCIDOS EN LA ENTRADA
    if(eleccion == 0):
        titulo = "DIJKSTRA BIDIRECCIONAL\n f= "+str(f)+" c= "+str(c)+" prob= "+str(probabilidad)+" seeds= "+str(semilla)+", "+str(semilla2)+", "+str(semilla3)
    if(eleccion == 1):
        titulo = "A* BIDIRECCIONAL\n f= "+str(f)+" c= "+str(c)+" prob= "+str(probabilidad)+" seeds= "+str(semilla)+", "+str(semilla2)+", "+str(semilla3)
    plt.title(titulo, fontdict={'fontsize':12}, pad=12)
   

    # DE ESTA FORMA ME PINTA EL CAMINO DE BLANCO Y SE DIFERENCIA DEL RESTO, AUNQUE EN EL VIDEO, NO ESTABA ESTO ANADIDO, POR TANTO, LAS PRUEBAS MOSTRADAS
    # SIGUEN OTRA GAMA DE COLOR, SIN EMBARGO EN LAS FOTOS DEL .ZIP SI QUE ESTA IMPLEMENTADO

    sb.heatmap(matrizPintar,mask=matrizPintar == 777.777,vmin=0,cmap=cmap,cbar_kws={'extend': 'min', 'extendrect': True}, annot=None, fmt="")

    plt.show()                                      # MUESTRA EL RESULTADO

else:
    print("No existe camino entre esos nodos")