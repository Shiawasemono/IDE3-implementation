import pandas as pd
import numpy as np

def entropia(matriz_datos,index=-1,valor=0):
	# Calculamos las clases existentes y las repeticiones en las mismas.
	valDif = matriz_datos[matriz_datos.columns[-1]].value_counts()
	# Convertimos la serie generada con la operación anterior en una lista de duplas
	# para trabajar con el número de apariciones de cada clase.
	valDif = list(zip(valDif.index, valDif.values))
	l = len(matriz_datos)
	E = 0
	if index == -1:
		#Estamos calculando la entropía de la variable de decisión
		for k in valDif:
			p = k[1]/l 
			E += p*np.log2(p)
	else:
		# Calculamos la entropía de una variable instanciada con un valor dado
		# Extracción del data frame filtrado por las dos columnas necesarias(index y variable de decisión)
		cnt = matriz_datos.groupby([matriz_datos.columns[index],matriz_datos.columns[-1]]).size()
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



raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'], 
        'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'], 
        'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger', 'Riani', 'Ali'], 
        'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]}

df = pd.DataFrame(raw_data)
print(Entropia(df, index=0, valor='Nighthawks'))


