import os, subprocess, sys

def main(output_directory, compressed_file):
    # Note that unrar-free only extracts into the current working directory,
    # hence the os.chdir() here
    try:
        os.chdir(output_directory)
        args = ['unrar', '-x', compressed_file]
        subprocess.call(args)
    except Exception as e:
        return e

if __name__ == '__main__':
    output_directory = sys.argv[1]
    compressed_file = sys.argv[2]
    exit(main(output_directory, compressed_file))
