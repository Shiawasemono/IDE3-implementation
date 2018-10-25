import pandas as pd
import numpy as np

def Entropia(matriz_datos,index=-1,valor=0):
	# Calculamos las clases existentes y las repeticiones en las mismas.
	valDif = matriz_datos[matriz_datos.columns[-1]].value_counts()
	# Convertimos la serie generada con la operación anterior en una lista de duplas
	# para trabajar con el número de apariciones de cada clase.
	valDif = list(zip(valDif.index, valDif.values))
	l = len(matriz_datos)
	if index == -1:
		#Estamos calculando la entropía de la variable de decisión
		E = 0
		for k in valDif:
			p = k[1]/l 
			E += p*np.log2(p)
	else:
		# Calculamos la entropía de una variable instanciada con un valor dado
		E = 0
		cnt = matriz_datos.groupby([matriz_datos.columns[index],matriz_datos.columns[-1]]).size()
		print(cnt)
	return -E

raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'], 
        'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'], 
        'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger', 'Riani', 'Ali'], 
        'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70, 25, 94, 57, 62, 70, 62, 70]}

df = pd.DataFrame(raw_data)
print(Entropia(df, index=0, valor='Dragoons'))
