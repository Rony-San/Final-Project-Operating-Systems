from multiprocessing import Pool
import time

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def mapper(chunk):
    words = chunk.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def reducer(results):
    word_count = {}
    for result in results:
        for word, count in result.items():
            word_count[word] = word_count.get(word, 0) + count
    return word_count
# 
def map_reduce(filename, num_chunks):
    text = read_file(filename)
    chunks = [text[i:i + len(text) // num_chunks] for i in range(0, len(text), len(text) // num_chunks)]
    start_time = time.time()
    with Pool(processes=num_chunks) as pool:
        mapped = pool.map(mapper, chunks)
    reduced = reducer(mapped)
    end_time = time.time()
    return reduced, end_time - start_time

if __name__ == "__main__":
    filename = "big1GB.txt"
    num_chunks =  2 # Limitando a 2 nodos
    word_count, elapsed_time = map_reduce(filename, num_chunks)
    # print("Word count:", word_count)
    print("Elapsed time:", elapsed_time, "seconds")

