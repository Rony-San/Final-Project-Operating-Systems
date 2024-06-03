from sys import stderr, stdout
import paramiko

# Definir los detalles de cada computadora
computadoras = [
    {"host": "192.168.1.8", "username": "kali", "password": "kali"},
    {"host": "192.168.1.9", "username": "kali", "password": "kali"}, #KALI SO 3
    {"host": "192.168.1.2", "username": "kali", "password": "kali"}, #KALI SO 1 
    {"host": "192.168.1.10", "username": "kali", "password": "kali"} #KALI SO 1 
]


archivo_local2 = "remoto_mapper.py"
carpeta_remota = "/home/kali/"

for comp in computadoras:
    try:

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


        ssh.connect(comp["host"], username=comp["username"], password=comp["password"])


        sftp = ssh.open_sftp()


        sftp.put(archivo_local2, f"{carpeta_remota}/{archivo_local2}")


        sftp.close()


        stdin, stdout, stderr = ssh.exec_command(f"python3 {carpeta_remota}/{archivo_local2}")


        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

  
        print("Output:", output)
        print("Errors:", errors)


        ssh.close()

        print(f"Archivos transferidos y ejecutados exitosamente en {comp['host']}")
    except Exception as e:
        print(f"No se pudo transferir y ejecutar los archivos en {comp['host']}: {str(e)}")
