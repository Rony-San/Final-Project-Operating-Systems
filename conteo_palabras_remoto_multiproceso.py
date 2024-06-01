import sys
import json
import os
from paramiko import SSHClient, AutoAddPolicy, SSHException
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_chunks(chunks):
    filenames = []
    os.makedirs("fragments", exist_ok=True)
    for i, chunk in enumerate(chunks):
        filename = f"fragments/fragment_{i}.txt"
        with open(filename, 'w') as file:
            file.write(chunk)
        filenames.append(filename)
    return filenames

def distribute_chunks(chunks, nodes):
    chunk_assignments = []
    for i, chunk in enumerate(chunks):
        node = nodes[i % len(nodes)]
        chunk_assignments.append((node, chunk))
    return chunk_assignments

def send_file(ssh, local_path, remote_path):
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()

def remote_map(node, local_chunk_file, remote_chunk_file):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        print(f"Conectando al nodo {node['host']}")
        ssh.connect(node['host'], username=node['username'], password=node['password'], timeout=120)
    except SSHException as e:
        print(f"Error conectando al nodo {node['host']}: {str(e)}")
        return {}, 0
    except Exception as e:
        print(f"Error general al conectar al nodo {node['host']}: {str(e)}")
        return {}, 0

    try:
        print(f"Enviando fragmento a {node['host']}")
        send_file(ssh, local_chunk_file, remote_chunk_file)
    except Exception as e:
        print(f"Error enviando archivo al nodo {node['host']}: {str(e)}")
        return {}, 0

    command = f"python3 remoto_mapper.py {remote_chunk_file}"
    try:
        print(f"Ejecutando comando en {node['host']}")
        start_time = time.time()
        stdin, stdout, stderr = ssh.exec_command(command, timeout=120)
        result = stdout.read().decode()
        error_output = stderr.read().decode()
        end_time = time.time()
        ssh.close()

        if error_output:
            print(f"Error en la ejecución remota en {node['host']}: {error_output}")

        execution_time = end_time - start_time
        return json.loads(result), execution_time
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON en el nodo {node['host']}: {str(e)}")
        print(f"Salida del comando: {result}")
        ssh.close()
        return {}, 0
    except SSHException as e:
        print(f"Error ejecutando el comando en {node['host']}: {str(e)}")
        ssh.close()
        return {}, 0
    except Exception as e:
        print(f"Error general al ejecutar el comando en {node['host']}: {str(e)}")
        ssh.close()
        return {}, 0

def reducer(results):
    word_count = {}
    for result in results:
        for word, count in result.items():
            word_count[word] = word_count.get(word, 0) + count
    return word_count

def map_reduce(filename, nodes):
    text = read_file(filename)
    num_chunks = len(nodes) * 4  # Aumenta el número de fragmentos
    chunks = [text[i:i + len(text) // num_chunks] for i in range(0, len(text), len(text) // num_chunks)]
    chunk_filenames = write_chunks(chunks)
    remote_chunk_filenames = [f"/home/kali/fragment_{i}.txt" for i in range(len(chunk_filenames))]
    chunk_assignments = distribute_chunks(list(zip(chunk_filenames, remote_chunk_filenames)), nodes)
    
    start_time = time.time()
    
    mapped_results = []
    node_times = {node['host']: {"start": None, "end": None} for node in nodes}
    with ThreadPoolExecutor(max_workers=len(nodes)) as executor:
        futures = [executor.submit(remote_map, node, local_chunk_file, remote_chunk_file) for node, (local_chunk_file, remote_chunk_file) in chunk_assignments]
        for future, (node, _) in zip(as_completed(futures), chunk_assignments):
            try:
                result, exec_time = future.result()
                mapped_results.append(result)
                host = node['host']
                if node_times[host]["start"] is None:
                    node_times[host]["start"] = time.time() - exec_time  # Assumes that the task was executed right after the future was submitted
                node_times[host]["end"] = time.time()
            except Exception as e:
                print(f"Error al procesar el nodo {node['host']}: {str(e)}")
    
    reduced = reducer(mapped_results)
    
    end_time = time.time()
    total_time = end_time - start_time
    node_execution_times = {node: times["end"] - times["start"] for node, times in node_times.items() if times["start"] is not None and times["end"] is not None}
    return reduced, total_time, node_execution_times

def save_result(word_count, output_filename):
    with open(output_filename, 'w') as file:
        for word, count in word_count.items():
            file.write(f"{word}: {count}\n")

def save_node_times(node_times, output_filename):
    with open(output_filename, 'w') as file:
        for node, exec_time in node_times.items():
            file.write(f"{node}: {exec_time} seconds\n")

if __name__ == "__main__":
    filename = "big.txt"  # Valor predeterminado
    output_filename = "word_count_result.txt"
    node_times_filename = "node_times.txt"
    
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        output_filename = sys.argv[2]
    elif len(sys.argv) == 4:
        filename = sys.argv[1]
        output_filename = sys.argv[2]
        node_times_filename = sys.argv[3]
    else:
        print("Uso: python3 conteo_palabras_remoto_multiproceso.py <archivo> [<output_file>] [<node_times_file>]")
        sys.exit(1)

    nodes = [
        {"host": "192.168.1.8", "username": "kali", "password": "kali"},
        # {"host": "192.168.1.9", "username": "kali", "password": "kali"},
        # {"host": "192.168.1.3", "username": "kali", "password": "kali"}
    ]

    word_count, elapsed_time, node_times = map_reduce(filename, nodes)
    
    save_result(word_count, output_filename)
    save_node_times(node_times, node_times_filename)
    
    print(f"Resultado guardado en {output_filename}")
    print(f"Tiempos de ejecución guardados en {node_times_filename}")
    print("Elapsed time:", elapsed_time, "seconds")
