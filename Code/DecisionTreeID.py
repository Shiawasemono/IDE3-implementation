import pandas as pd
import numpy as np
import anytree as at
import operator

def entropia(matriz_datos,col='',valor=0):
	# Calculamos las clases existentes y las repeticiones en las mismas.
	if(col == ''):
		col = matriz_datos.columns[-1]
	valDif = matriz_datos[col].value_counts()
	# Convertimos la serie generada con la operación anterior en una lista de duplas
	# para trabajar con el número de apariciones de cada clase.
	valDif = list(zip(valDif.index, valDif.values))
	l = len(matriz_datos)
	E = 0
	if col == matriz_datos.columns[-1]:
		#Estamos calculando la entropía de la variable de decisión
		for k in valDif:
			p = k[1]/l 
			E += p*np.log2(p)
	else:
		# Calculamos la entropía de una variable instanciada con un valor dado
		# Extracción del data frame filtrado por las dos columnas necesarias(index y variable de decisión)
		cnt = matriz_datos.groupby([col,matriz_datos.columns[-1]]).size()
		# Zipeo de la información
		dic = dict(zip(cnt.index,cnt.values))
		# Array conla información que será filtrada por valor
		a = []
		for k in dic:
			if(k[0] == valor):
				a.append(dic[k])
		
		# Cálculo de la entropía
		l = len(a)
		for k in a:
			p = k/l
			E += p*np.log2(p)
			
	return -E

def ganancia(matriz_datos,col):
	# Ganancia de un valor se define como: EntropiaGen + Sum (- valor/filastotales * entropia(matriz,indice,valor))
	enGen = entropia(matriz_datos)
	filas = len(matriz_datos)
	valDif = matriz_datos[col].value_counts()
	valDif = list(zip(valDif.index,valDif.values))
	Sum = 0
	for k in valDif:
		p = k[1]/filas
		Sum -= p*entropia(matriz_datos,col,k[0])
	G = enGen + Sum
	return G

def DecisionTreeID(nombre_fichero):
    matriz_datos = pd.read_csv(nombre_fichero)
    
    # while not arbol_terminado:
    #     dict_ganancias = {} # creo diccionario de ganancias vacío
    #     atributos = matriz_datos.loc[matriz_datos.columns[:-1]]
    #     for column in atributos: # por cada columna que me quede en la matriz de datos
    #         entropias = []
    #         # calculo entropia de cada caso
    #         dict_ganancias[column] = ganancia(entropias) # calculo ganancia y la meto en el diccionario
    #     ganancia_maxima = max(dict_ganancias.items(), key=operator.itemgetter(1))[0] # cojo ganancia maxima
    #     # inserto nuevos nodos en arbol
	# 	#TODO: Antes de eliminar la columna, hay que eliminar las filas que contienen el valor del proximo nodo
    #     matriz_datos = matriz_datos.drop(columns = [ganancia_maxima]) # actualizo matriz_datos (elimino la columna escogida como atributo)
	# 	#TODO: No hay que considerar que el arbol esta acabado cuando solo hay una columna, sino cuando hemos explorado todos los valores del primer nodo.
	# 	# Backtracking HIGHLY recommended, o al menos la idea de la partición en miniárboles (que no deja de ser backtracking)
    #     arbol_terminado = len(matriz_datos.columns) == 1 # actualizo arbol_terminado

    #     # Borrar esto:
    #     print('asd')
    #     arbol_terminado = True

    # return matriz_datos
    return decisionTree(matriz_datos)

def reducir_matriz(matriz,columna,fila):
    matriz_aux = matriz[matriz.columna != fila]
    matriz_aux = matriz_aux.drop(columns = [columna])

    return matriz_aux

def decisionTree(matriz_datos, padre=None, rama=''):
	# :param pandas.DataFrame matriz_datos es la matriz a partir de la cual generar el nodo siguiente
	# :param str padre nodo padre del nodo a generar (en este caso será la columna de la que salió el arco)
    if matriz_datos.size == 3:
        #TODO: Caso base
        pass
    variables = matriz_datos.loc[matriz_datos.columns[:-1]]

    ganancia_max = ['',0]
    for columna in variables:
        ganancia_act = ganancia(matriz_datos, columna)
        if ganancia_max[1] < ganancia_act:
            ganancia_max = [columna, ganancia_act]

    if rama == '':
        nodo = at.Node(ganancia_max[0])
    else:
        nodo = at.Node(ganancia_max[0],padre,rama)

    hijos = matriz_datos[ganancia_max[0]].value_counts()
    hijos = list(hijos.index)
    
    for hijo in hijos:
        matriz_hijo = reducir_matriz(matriz_datos,ganancia_max[0],hijo)
        decisionTree(matriz_hijo, ganancia_max[0], hijo)

    return nodo
    