import java.util.Scanner;


/*
 * Codigo correspondiente a la implementacion del algoritmo quick sort utilizando un unico array puesto que es mejor que con dos arrays
 * y ademas recibe como parametro un valor c, este algoritmo va a hallar los tamaños de las partes izquierda y derecha del pivote,
 * si estas son de mayor tamaño que c, entonces las ordena con quicksort, y si es mejor que c las ordena con insertionsort
 */

public class QuickSortValorC {

	public static void main(String[] args) {
		Scanner en = new Scanner(System.in);  //Se crea un objeto Scanner
		System.out.println("Introduce la coordenada X con el que vas a comparar: ");
		double x = en.nextDouble();
		System.out.println("Introduce la coordenada Y con el que vas a comparar: ");
		double y = en.nextDouble();
		double input [][]= {{x},{y}};
		System.out.println("Introduce el numero de vectores a comparar: "); 
		int tam = en.nextInt();
		//double componentes[][] = {{4,5},{1,2},{9,10},{6,7},{14,16},{0,1}};
		double [][] componentes = new double[tam][2];
		for(int j=0;j<tam;j++) {                      								//Rellena el array anterior de vectores generados de manera random 
			componentes[j][0] = Math.random()*100;    								// Vectores que van tanto la componente x como la y, desde 0 hasta 100
			componentes[j][1] = Math.random()*100;
		}
		System.out.println("\nA partir de que tamaño 'c' quieres usar insertionSort: ");
		int lim = en.nextInt();
		long inicio = System.nanoTime();
		double solucion[][] = quickSort(input, componentes, 0, componentes.length-1,lim);
		long fin = System.nanoTime() - inicio;
		System.out.println("El vector ordenado por angulos respecto a ("+input[0][0]+","+input[1][0]+") es: \n");
		System.out.print("\n{");
		for(int i=0;i<componentes.length;i++) {
			System.out.print("{"+solucion[i][0]+","+solucion[i][1]+"},");
		}
		System.out.print("}\n");
		System.out.println("\nEl tiempo en ordenar los vectores es: "+ 1e-9*fin+" segundos");
		en.close();
	
	}
	
	/*
	 * Metodo que se encarga de hallar el angulo entre el vector que se pide como entrada y los del array de  vectores
	 */
	
	public static double angulo(double[][] A, double x1, double y1){
		double angulo = 0;
		double x = A[0][0];
		double y = A[1][0];
		angulo = Math.acos((x*x1 + y*y1)/((Math.sqrt((Math.pow(x, 2)+(Math.pow(y, 2)))))*(Math.sqrt((Math.pow(x1, 2)+(Math.pow(y1, 2)))))));
		angulo = (angulo*180)/Math.PI;
		return angulo;
	}

	public static double[][] quickSort(double[][] entrada, double[][] vectores, int min, int max,int c) {  
		if(max-min+1 > c) {
			if (min >= 0 && max >= 0 && min < max) { //Comprueba si min < max y que sean valores positivos
				int p = partition(entrada,vectores, min,max); 	   //Realiza la particion del array y haya el indice del pivote
				quickSort(entrada, vectores, min, p - 1,c);     	   //Partición del lado izquierdo del pivote
		    	quickSort(entrada, vectores, p + 1, max,c); 		   //Partición del lado derecho del pivote
			}
		}else {
			insertionSort(entrada,vectores,min,max);
	}
		return vectores;								   //Retorna el array ordenado
	}
	
	// Metodo que se encarga de dividir el array en dos partes
	
	public static int partition(double[][] A,double[][] B,int min,int max) { 
		  double pivot = angulo(A,B[max][0],B[max][1]);    				//El pivote es el angulo, del ultimo elemento del array con el vector solicitado como entrada
		  int i = min - 1;							//Indice del pivote
		  for (int j = min; j<=max;j++) {			//Recorre la particion
		    if (angulo(A,B[j][0],B[j][1]) <= pivot) {					//Si el angulo del actual es menor o igual que el angulo pivote
		      i = i + 1;							//Mueve el indice del pivote una posicion alante
		      double pivotx = B[i][0];				//Intercambia la componente X del vector del array desordenado
		      double pivoty = B[i][1];				//Intercambia la componente Y del vector del array desordenado
		      B[i][0] = B[j][0];					//Swaps
		      B[i][1] = B[j][1];
		      B[j][0] = pivotx;
		      B[j][1] = pivoty;
		    }
		    }
		  return i; 								//Retorna el indice del pivote
	}
	
	public static double[][] insertionSort(double[][] A,double[][] B,int min, int max) {
		int i = min;  								//Inicia en min
		while(i <= max) {
			while(i < B.length) { 						//Recorra todo el array de angulos
				double vx= B[i][0]; 				//Componente X del vector que se encuentra en la posicion m
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
		}
		return B;
	}
}
