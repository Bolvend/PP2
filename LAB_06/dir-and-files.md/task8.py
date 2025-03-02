import os

file_path = "file_to_delete.txt"

if os.path.exists(file_path):
    if os.access(file_path, os.W_OK):
        os.remove(file_path)
        print(f"File {file_path} delete.")
    else:
        print(f"You can't delete this file {file_path}.")
else:
    print(f"File {file_path} doesn't exist.")
