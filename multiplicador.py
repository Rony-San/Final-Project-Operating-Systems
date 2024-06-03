import os

def create_large_file(input_file, output_file, desired_size_gb):
    # Convert desired size from GB to bytes
    desired_size_bytes = desired_size_gb * 1024 * 1024 * 1024
    
    # Read the content of the input file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Calculate how many times the content needs to be repeated to reach the desired size
    content_size_bytes = len(content.encode('utf-8'))
    repetitions = int(desired_size_bytes // content_size_bytes + 1)

    # Write the repeated content to the output file
    with open(output_file, 'w') as f:
        for _ in range(repetitions):
            f.write(content)
            # Check the size of the output file and stop if it has reached the desired size
            if os.path.getsize(output_file) >= desired_size_bytes:
                break

    # Verify the final size of the output file
    final_size_bytes = os.path.getsize(output_file)
    
    # Print the final size of the output file in GB
    print(f"Tamaño del archivo resultante: {final_size_bytes / (1024 * 1024 * 1024):.2f} GB")

# File paths and desired size
input_file = "big.txt"
output_file = "big2GB.txt"
desired_size_gb = 2  # 2 GB

# Create the large file
create_large_file(input_file, output_file, desired_size_gb)
