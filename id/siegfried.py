from __future__ import print_function

import json
import subprocess
import sys

def file_tool(path):
    return subprocess.check_output(['file', path]).strip()

def main(f):
    try:
        result = json.loads(subprocess.check_output(["sf", "-json", f]))
    except subprocess.CalledProcessError as e:
        print("Siegfried exited {} and no format was found.".format(e.returncode), file=sys.stderr)
        return 1

    match = result['files'][0]
    if len(match['matches']) == 0 or match['matches'][0]['puid'] == 'UNKNOWN':
        if "text" in file_tool(f):
            print("x-fmt/111")
        else:
            print("Siegfried exited 0 but no format was found.", file=sys.stderr)
            return 1
    else:
        print(match['matches'][0]['puid'])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
