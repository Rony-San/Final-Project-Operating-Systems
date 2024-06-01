import os

# Ruta del archivo de texto inicial
archivo_inicial = "big.txt"

# Ruta del archivo de texto resultante
archivo_resultante = "texto_resultante.txt"
# 
# Tamaño máximo en bytes (2 GB)
tamanio_maximo = 2 * 1024 * 1024 * 1024  # 2 GB en bytes

# Leer el contenido del archivo inicial
with open(archivo_inicial, 'r') as f:
    contenido = f.read()

# Multiplicar el contenido hasta que el tamaño total sea aproximadamente 2 GB
contenido_multiplicado = ""
while len(contenido_multiplicado.encode('utf-8')) < tamanio_maximo:
    contenido_multiplicado += contenido

# Escribir el contenido multiplicado en el archivo resultante
with open(archivo_resultante, 'w') as f:
    f.write(contenido_multiplicado)

# Verificar el tamaño final del archivo resultante
tamanio_archivo_resultante = os.path.getsize(archivo_resultante)

# Imprimir el tamaño final del archivo resultante en GB
print(f"Tamaño del archivo resultante: {tamanio_archivo_resultante / (1024 * 1024 * 1024):.2f} GB")
