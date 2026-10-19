import os
from pathlib import Path


print(len(item_path))
print(item_path)
print(type(item_path))

with open(item_path, "rb") as file_open:
    file_bytes = file_open.read()
    print(file_bytes)
    print(len(file_bytes))
