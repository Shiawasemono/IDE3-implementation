import pandas as pd
import operator

def entropia(matriz_datos):
        return 1

def ganancia(input):
    return 1

def DecisionTreeID(nombre_fichero):
    matriz_datos = pd.read_csv(nombre_fichero)
    matriz_datos_original = pd.read_csv(nombre_fichero) # Realmente necesario? Demanding?

    # variable_decision = matriz_datos[matriz_datos.columns[-1]] # "La variable de decisión aparecerá la última en la lista (...)"
    entropia_inicial = entropia(matriz_datos)
    
    arbol_terminado = False
    arbol = None
    padre_actual = None
    siguiente_nodo = None
    
    while not arbol_terminado:
        dict_ganancias = {} # creo diccionario de ganancias vacío
        atributos = matriz_datos.loc[matriz_datos.columns[:-1]]
        for column in atributos: # por cada columna que me quede en la matriz de datos
            entropias = []
            # calculo entropia de cada caso
            dict_ganancias[column] = ganancia(entropias) # calculo ganancia y la meto en el diccionario
        ganancia_maxima = max(dict_ganancias.items(), key=operator.itemgetter(1))[0] # cojo ganancia maxima
        # inserto nuevos nodos en arbol
		#TODO: Antes de eliminar la columna, hay que eliminar las filas que contienen el valor del proximo nodo
        matriz_datos = matriz_datos.drop(columns = [ganancia_maxima]) # actualizo matriz_datos (elimino la columna escogida como atributo)
		#TODO: No hay que considerar que el arbol esta acabado cuando solo hay una columna, sino cuando hemos explorado todos los valores del primer nodo.
		# Backtracking HIGHLY recommended, o al menos la idea de la partición en miniárboles (que no deja de ser backtracking)
        arbol_terminado = len(matriz_datos.columns) == 1 # actualizo arbol_terminado

        # Borrar esto:
        print('asd')
        arbol_terminado = True

    return matriz_datos

def decisionTree(matriz_datos, padre):
	'''
	:param pandas.DataFrame matriz_datos es la matriz a partir de la cual generar el nodo siguiente
	:param str padre nodo padre del nodo a generar (en este caso será la columna de la que salió el arco)
	'''

	# Al hacer backtracking no necesitamos devolver nada, simplemente salir de la funcion para que continúe