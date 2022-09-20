import java.util.Scanner;


/*
 * Codigo correspondiente a la implementacion del algoritmo quicksort utilizando 2 arrays
 * Uno que contiene vectores que se van a tener que ordenar, y otro que contiene los angulos con respecto al vector que se
 * pide como entrada, en esta implementacion se usa mas memoria pero es mas rapida hasta un determinado valor de n (nº entradas)
 * y a partir de ese n el tiempo aumenta muy rapidamente.
 * Usa mas memoria, pero mas veloz hasta un n determinado
 */


public class QuickSort2Arrays {
		public static void main(String[] args){
			Scanner en = new Scanner(System.in); 
			System.out.println("Introduce la coordenada X con el que vas a comparar: ");
			double x = en.nextDouble();
			System.out.println("Introduce la coordenada Y con el que vas a comparar: "); 
			double y = en.nextDouble();
			double input [][]= {{x},{y}};
			System.out.println("Introduce el numero de vectores a comparar: "); 		//Pide el tamaño de la entrada
			int tam = en.nextInt();
			double [][] componentes = new double[tam][2]; 								//Crea un array del tamano para que quepan los n vectores
			for(int j=0;j<tam;j++) {                      								//Rellena el array anterior de vectores generados de manera random 
				componentes[j][0] = Math.random()*100;    								// Vectores que van tanto la componente x como la y, desde 0 hasta 100
				componentes[j][1] = Math.random()*100;
			}
			double angulos[] = new double[componentes.length]; 							//Crea un array donde se van a almacenar los angulos,en orden
			for(int i=0;i<componentes.length;i++) {
					angulos[i] = angulo(input,componentes[i][0],componentes[i][1]); 	//Se rellena con los angulos hallados, pasando como parametro
			}																			//el vector que sirve de referencia y el primer vector del
																						//aaray autogenerado de vectores
			long inicio = System.nanoTime();											//Contiene el tiempo, cuando el programa justo empieza a ordenar el vector
			double solucion[][] = quickSort(angulos,componentes,0,componentes.length-1);//Contiene el array de vectores ordenado, la solucion
			long fin = System.nanoTime() - inicio;										//De la resta se obtiene el tiempo que ha tardado el programa en ordenar el array
			
			System.out.println("\nEl vector ordenado por angulos respecto a ("+input[0][0]+","+input[1][0]+") es: \n");
			System.out.print("{");
			for(int i=0;i<componentes.length;i++) {      								//Este bucle printea el array solucion
				System.out.print("{"+solucion[i][0]+","+solucion[i][1]+"},");
			}
			System.out.print("}\n");
			
			System.out.println("\nEl tiempo en ordenar los vectores es: "+ 1e-9*fin+" segundos"); //Printeo el tiempo que ha tardado en ordenarlo
			en.close();
		}
		
		/*
		 * Es la funcion que se encarga de hallar los angulos,  de los vectorees del array desordenado con respecto al vector
		 * recibe el array A, que contiene la componente X e Y del vector que se pide como entrada, para hallar los angulos
		 * y la coordenada X e Y de los vectores del array desordenado.
		 * 
		 * Este metodo, recibe en orden los vectores del array desordenado, de esta forma el primer angulo que se obtiene es
		 * el angulo del primer vector del array desordenado con el vector pediddo como entrada, y en el main los almacena en el orden
		 * que se obtienen, sabiendo asi que el angulo en la posicion i del array de angulos, va a ser el angulo formado por el vector de
		 * entrada con el vector de la posicion i del array de vectores desordenados.
		 */
		public static double angulo(double[][] A, double x1, double y1){
			double angulo = 0;					//Inicializamos la variable
			double x = A[0][0]; 				//Coordenada x del vector que se pide como entrada
			double y = A[1][0];					//Coordenada y del vector que se pide como entrada
			angulo = Math.acos((x*x1 + y*y1)/((Math.sqrt((Math.pow(x, 2)+(Math.pow(y, 2)))))*(Math.sqrt((Math.pow(x1, 2)+(Math.pow(y1, 2)))))));
			angulo = (angulo*180)/Math.PI; 		//Convierte el angulo de radianes a grados
			return angulo;
		}

		/*
		 * Metodo de ordenacion recursivo
		 */
		
		public static double[][] quickSort(double[] A, double[][] B, int min, int max) {  
			  if (min >= 0 && max >= 0 && min < max) { //Comprueba si los indices estan en el orden correcto
			    int p = partition(A,B, min,max); 	   //Realiza la particion del array y haya el indice del pivote
			    quickSort(A, B, min, p - 1);     	   //Partición del lado izquierdo del pivote
			    quickSort(A, B, p + 1, max); 		   //Partición del lado derecho del pivote
			  }
			return B;								   //Retorna el array ordenado
		}
			
		// Metodo que se encarga de dividir el array en dos partes
		
		public static int partition(double[] A,double[][] B,int min,int max) { 
			  double pivot = A[max];    				//El pivote es el ultimo elemento del  array de angulos
			  int i = min - 1;							//Indice del pivote
			  for (int j = min; j<=max;j++) {			//Recorre la particion
			    if (A[j] <= pivot) {					//Si el elemento actual es menor o igual que el pivote
			      i = i + 1;							//Mueve el indice del pivote una posicion alante
			      double cambio = A[i];					//Intercambia el angulo
			      double pivotx = B[i][0];				//Intercambia la componente X del vector del array desordenado
			      double pivoty = B[i][1];				//Intercambia la componente Y del vector del array desordenado
			      B[i][0] = B[j][0];					//Swaps
			      B[i][1] = B[j][1];
			      B[j][0] = pivotx;
			      B[j][1] = pivoty;
			      A[i] = A[j];
			      A[j] = cambio;
			    }}
			  return i; 								//Retorna el indice del pivote
		}
}

