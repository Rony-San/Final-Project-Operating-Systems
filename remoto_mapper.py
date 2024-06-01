import sys
import json



def mapper(chunk):
    words = chunk.split()
    word_count = {}
    for word in words:
        word = word.strip(",.?!;()[]{}\"'").lower()
        if word:
            word_count[word] = word_count.get(word, 0) + 1
    return word_count

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Uso: python3 remoto_mapper.py <chunk_file>")
            sys.exit(1)

        chunk_file = sys.argv[1]
        with open(chunk_file, 'r') as file:
            chunk = file.read()

        result = mapper(chunk)

        # Print results as JSON string
        print(json.dumps(result))
    except Exception as e:
        print(f"Error durante la ejecución de mapper: {str(e)}", file=sys.stderr)
