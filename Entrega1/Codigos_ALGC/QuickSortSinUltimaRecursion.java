import java.util.Scanner;


/*
 * Codigo correspondiente a la implementacion del algoritmo quick sort utilizando un unico array, pero en este algorimo
 * realizo los cambios determinados para eliminar la ultima recursividad.
 */


public class QuickSortSinUltimaRecursion {
		public static void main(String[] args) {
			Scanner en = new Scanner(System.in);  										 //Se crea un objeto Scanner
			System.out.println("Introduce la coordenada X con el que vas a comparar: "); //Se solicita la coordenada X del vector que va a servir para hallar los angulos
			double x = en.nextDouble();
			System.out.println("Introduce la coordenada Y con el que vas a comparar: "); //Se solicita la coordenada Y del vector que va a servir para hallar los angulos
			double y = en.nextDouble();
			double input [][]= {{x},{y}};
			System.out.println("Introduce el numero de vectores a comparar: "); 		//Pide el tamaño de la entrada
			int tam = en.nextInt();
			/*double[][] componentes = { { 4, 6 }, { 3, 4 }, { 8, 9 }, { 5, 6 }, { 4.5, 0.3 },
			        { 9.8, 7.2 }, { 4.1, 8.5 },
			         { 1.1, 6.8 }, { 4.4, 5.8 }, { 4, 7.7 } };*/
			double [][] componentes = new double[tam][2]; 								//Crea un array del tamano para que quepan los n vectores
			for(int j=0;j<tam;j++) {                      								//Rellena el array anterior de vectores generados de manera random 
				componentes[j][0] = Math.random()*100;    								// Vectores que van tanto la componente x como la y, desde 0 hasta 100
				componentes[j][1] = Math.random()*100;
			}															
				
			long inicio = System.nanoTime();											//Contiene el tiempo, cuando el programa justo empieza a ordenar el vector
			double solucion[][] = quickSort(input,componentes,0,componentes.length-1);  //Contiene el array de vectores ordenado, la solucion
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
		 * Metodo que se encarga de hallar el angulo entre el vector que se pide como entrada y los del array de  vectores
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
		 * Metodo de ordenacion eliminando la recursion final
		 */
		
		public static double[][] quickSort(double[][] A, double[][] B, int min, int max) {  
			  while(min >= 0 && max >= 0 && min < max) { 							//Introducimos un while en vez de un if que hace que se repita para quitar la recursividad
				    int p = partition(A,B, min,max); 	    //Realiza la particion del array y haya el indice del pivote
				    quickSort(A, B, min, p - 1);     	    //Partición del lado izquierdo del pivote
				    min = p +1;								//voy sumando uno al pivote, y de esta forma modifico min, para que lo ordene sin necesidad
				    										//de hacer recursiva la recursion final, modificando el valor de la variable
			  }
			return B;								   		//Retorna el array ordenado
		}
		
		// Metodo que se encarga de dividir el array en dos partes
		
		public static int partition(double[][] A,double[][] B,int min, int max) { 
			  double pivot = angulo(A,B[max][0],B[max][1]);    				//El pivote es el angulo, del ultimo elemento del array con el vector solicitado como entrada
			  int i = min - 1;												//Indice del pivote
			  for (int j = min; j<=max;j++) {								//Recorre la particion
			    if (angulo(A,B[j][0],B[j][1]) <= pivot) {					//Si el angulo del actual es menor o igual que el angulo pivote
			      i = i + 1;												//Mueve el indice del pivote una posicion alante
			      double pivotx = B[i][0];									//Intercambia la componente X del vector del array desordenado
			      double pivoty = B[i][1];									//Intercambia la componente Y del vector del array desordenado
			      B[i][0] = B[j][0];										//Swaps
			      B[i][1] = B[j][1];
			      B[j][0] = pivotx;
			      B[j][1] = pivoty;
			    }
			    }
			  return i; 								//Retorna el indice del pivote
		}
}
