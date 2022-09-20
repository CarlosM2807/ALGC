import java.util.Scanner;


/*
 * Codigo correspondiente a la implementacion del algoritmo insertion sort utilizando un unico array
 * El que contiene vectores que se van a tener que ordenar, con respecto al vector que se pide como entrada,
 * en esta implementacion se usa menos memoria, entorno a la mitad puesto que es un array en vez de dos
 * pero es mas lento hasta un determinado valor de n (nº entradas)
 * y a partir de ese n el tiempo aumenta pero no tan rapidamente como en la otra implementacion.
 * Usa menos memoria, pero mas lento hasta un n determinado
 */


public class InsertionSort1Array {

	public static void main(String[] args) {
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
		long inicio = System.nanoTime();											//Contiene el tiempo, cuando el programa justo empieza a ordenar el vector
		double solucion[][] = insertionSort(componentes,input); 					//Contiene el array de vectores ordenado, la solucion
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
	 * Metodo insertion sort, recibe como parametro el vector que se solicita como entrada y el array de vectores desordenados
	 * debido a la relacion explicada en el metodo anterior, para ordenar el array de vectores va hallando en el propio metodo,
	 * los angulos necesarios, es decir, no los almacena y los ordena sino que los ordena segun los va hallando
	 */
	
	public static double[][] insertionSort(double[][] B, double[][] A) {
		int i = 1;  								//Inicia en 1, para que j pueda tomar el valor 0
		while(i < B.length) { 						//Recorra todo el array de angulos
				double vx= B[i][0]; 	            //Componente X del vector que se encuentra en la posicion m
				double vy= B[i][1]; 				//Componente Y del vector que se encuentra en la posicion m
				double x = angulo(A,vx,vy); 		// X es el Valor del angulo de ese vector (vx,vy)
				int j = i - 1;   					// j va a contener el indice del elemento anterior
			while(j >= 0 && angulo(A,B[j][0],B[j][1]) > x) { 	//Si el valor del angulo anterior, es mayor que el del angulo posterior y j >= 0 entonces
				B[j+1][0] = B[j][0];  				//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
				B[j+1][1] = B[j][1];  				//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
				j = j - 1;
			}
			B[j+1][0] = vx; 						//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
			B[j+1][1] = vy; 						//Aplicamos el cambio pero teniendo en cuenta que son 2 componentes, para ordenar el de vectores
			i = i + 1;								//Aumentamos en 1 la variable i para que continue con el bulce while	
		}
		return B;
	}
}