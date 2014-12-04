import os.path
import subprocess
import sys

def file_tool(path):
    return subprocess.check_output(['file', path]).strip()

(_, extension) = os.path.splitext(sys.argv[1])
if extension:
    print extension.lower()
else:
    # Plaintext files frequently have no extension, but are common to identify.
    # file is pretty smart at figuring these out.
    file_output = file_tool(sys.argv[1])
    if 'text' in file_output:
        print '.txt'
