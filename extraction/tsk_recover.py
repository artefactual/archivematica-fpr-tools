from __future__ import print_function
import re
import subprocess
import sys

def extract(package, outdir):
    # -a extracts only allocated files; we're not capturing unallocated files
    try:
        process = subprocess.Popen(['tsk_recover', package, '-a', outdir],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = process.communicate()

        match = re.match(r'Files Recovered: (\d+)', stdout.splitlines()[0])
        if match:
            if match.groups()[0] == '0':
                raise Exception('tsk_recover failed to extract any files with the message: {}'.format(stdout))
            else:
                print(stdout)
    except Exception as e:
        return e

    return 0

def main(package, outdir):
    return extract(package, outdir)

if __name__ == '__main__':
    package = sys.argv[1]
    outdir = sys.argv[2]
    sys.exit(main(package, outdir))
