import sys

import pandas as pd

from carga import cargar_datos


clientes, ventas = cargar_datos()

if sys.argv[1] == "ventas":
    df = ventas
elif sys.argv[1] == "clientes":
    df = clientes
else:
    print('Escribe "ventas" o "clientes" como argumento.')
    sys.exit(1)

print("Dimensiones:", df.shape)
df.info()
print(df.describe())

if sys.argv[1] == "ventas":
    datos = pd.read_csv("Data/raw/ventas.csv", usecols=["producto", "total"])
    print(datos)
