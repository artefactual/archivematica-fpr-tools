import subprocess
import sys

# Python 2/3 compatibility
try:
    range = xrange
except NameError:
    pass

MAX_TRIES = 16


def convert(document, target, max_tries=MAX_TRIES):
    """
    Attempt to convert a document into a PDF at the target location.

    This continues up to max_tries times; it's possible for initial calls
    to fail due to delays in spinning up a LibreOffice server, where
    retries may succeed.
    """
    for _ in range(0, max_tries):
        try:
            # SelectPdfVersion=1 converts to PDF/A-1a, instead of
            # the default PDF 1.4
            subprocess.check_call(['unoconv', '-eSelectPdfVersion=1',
                                   '--output', target, document])
            return 0
        except subprocess.CalledProcessError:
            continue

    return 1

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file-full-name", dest="input")
    parser.add_argument("--output-file-path", dest="output")
    args, _ = parser.parse_known_args()

    sys.exit(convert(args.input, args.output + '.pdf'))
