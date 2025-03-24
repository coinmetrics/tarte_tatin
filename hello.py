import os
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_dummy_files(directory):
    """
    Creates three text files with random content in the specified directory.
    """
    for i in range(3):
        filename = f"random_file_{i + 1}.txt"
        filepath = os.path.join(directory, filename)
        content = generate_random_string(random.randint(100, 500))  # Random content length
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created file: {filepath}")

if __name__ == "__main__":
    # Get directory from environment variable, default to /tmp/
    output_directory = os.environ.get("OUTPUT_DIR", "/tmp/")

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    create_dummy_files(output_directory)
    print("Dummy files created.")
