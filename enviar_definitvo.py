from sys import stderr, stdout
import paramiko

# Definir los detalles de cada computadora
computadoras = [
    {"host": "192.168.1.8", "username": "kali", "password": "kali"},
    {"host": "192.168.1.9", "username": "kali", "password": "kali"}, #KALI SO 3
    {"host": "192.168.1.3", "username": "kali", "password": "kali"} #KALI SO 1 
]

# Ruta del archivo que deseas transferir
archivo_local2 = "remoto_mapper.py"
carpeta_remota = "/home/kali/"
# 
# Iterar sobre cada computadora y transferir el archivo
for comp in computadoras:
    try:
        # Crear una instancia de SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar a la computadora remota
        ssh.connect(comp["host"], username=comp["username"], password=comp["password"])

        # Crear una instancia de SFTPClient
        sftp = ssh.open_sftp()

        # Transferir los archivos a la carpeta remota
        sftp.put(archivo_local2, f"{carpeta_remota}/{archivo_local2}")

        # Cerrar la conexión SFTP
        sftp.close()

        # Ejecutar el script en la carpeta remota
        stdin, stdout, stderr = ssh.exec_command(f"python3 {carpeta_remota}/{archivo_local2}")

        # Obtener salida del comando ejecutado
        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

        # Imprimir la salida y los errores
        print("Output:", output)
        print("Errors:", errors)

        # Cerrar la conexión SSH
        ssh.close()

        print(f"Archivos transferidos y ejecutados exitosamente en {comp['host']}")
    except Exception as e:
        print(f"No se pudo transferir y ejecutar los archivos en {comp['host']}: {str(e)}")
