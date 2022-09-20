import java.util.*;

/*
 * Codigo correspondiente a la implementacion del algoritmo insertion sort utilizando 2 arrays
 * Uno que contiene vectores que se van a tener que ordenar, y otro que contiene los angulos con respecto al vector que se
 * pide como entrada, en esta implementacion se usa mas memoria pero es mas rapida hasta un determinado valor de n (nº entradas)
 * y a partir de ese n el tiempo aumenta muy rapidamente.
 * Usa mas memoria, pero mas veloz hasta un n determinado
 */


public class InsertionSort2Arrays {
	public static void main(String[] args){
		
		Scanner en = new Scanner(System.in);  
		System.out.println("Introduce la coordenada X con el que vas a comparar: "); 
		double x = en.nextDouble();
		System.out.println("Introduce la coordenada Y con el que vas a comparar: "); 
		double y = en.nextDouble();
		double input [][]= {{x},{y}};
		System.out.println("Introduce el numero de vectores a comparar: "); 		
		int tam = en.nextInt();
		//Crea un array del tamano para que quepan los n vectores
		double [][] componentes = new double[tam][2]; 								
		//Rellena el array anterior de vectores generados de manera random, cada componente puede tomar el valor de 0 hasta 100
		for(int j=0;j<tam;j++) {                      								
			componentes[j][0] = Math.random()*100;    								
			componentes[j][1] = Math.random()*100;
		}
		//Crea un array donde se van a almacenar los angulos,en orden
	    double angulos[] = new double[componentes.length]; 	
	    //Se rellena con los angulos hallados, pasando como parametro el vector que sirve de referencia y el primer vector del array de vectores																
		for(int i=0;i<componentes.length;i++) {
				angulos[i] = angulo(input,componentes[i][0],componentes[i][1]); 	
		}
		long inicio = System.nanoTime();											//Contiene el tiempo, cuando el programa justo empieza a ordenar el vector
		double solucion[][] = insertionSort(angulos,componentes); 					//Contiene el array de vectores ordenado, la solucion
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
	 * Metodo insertion sort, recibe como parametro el array de angulos y el array de vectores desordenados
	 * debido a la relacion explicada en el metodo anterior, para ordenar el array de vectores bastaria con ordenar el de angulos
	 * y realizar exactamente los mismos cambios en el de vectores, solo que aplicando el cambio a dos componentes las X e Y de los vectores
	 */
	
	public static double[][] insertionSort(double[] A, double[][] B) {
		int i = 1;  						//Inicia en 1, para que j pueda tomar el valor 0
		while(i < A.length) { 				//Recorra todo el array de angulos
			for(int m=1;m<B.length;m++) { 	//Recorra todo el array de vectores
					double vx= B[m][0]; 	//Componente X del vector que se encuentra en la posicion m
					double vy= B[m][1]; 	//Componente Y del vector que se encuentra en la posicion m
					double x = A[i]; 		// X es el Valor del angulo de ese vector (xx,vy)
					int j = i - 1;   		// j va a contener el indice del elemento anterior
			while(j >= 0 && A[j] > x) { 	//Si el valor del angulo anterior, es mayor que el del angulo posterior y j >= 0 entonces
				A[j+1] = A[j];        		//El posterior, toma el valor del anterior, para ordenar el de angulos
				B[j+1][0] = B[j][0];  		//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
				B[j+1][1] = B[j][1];  		//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
				j = j - 1;
			}
			A[j+1] = x;						//El valor del angulo posterior entonces pasa a valer X
			B[j+1][0] = vx; 				//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
			B[j+1][1] = vy; 				//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
			i = i + 1;						//Aumentamos en 1 la variable i para que continue con el bulce while
			}	
		}
		return B;
	}
}
