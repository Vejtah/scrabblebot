import os

letters = ["_", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

parent_folder = "/home/malina/sb/scrabblebot/code/networks/letters/train"

for folder in letters:
    subfolder_name = folder

    # Create the full path for the subfolder
    subfolder_path = os.path.join(parent_folder, subfolder_name)

    # Create the subfolder; exist_ok=True prevents errors if the folder already exists
    os.makedirs(subfolder_path, exist_ok=True)

    print(f"Subfolder created at: {subfolder_path}")
