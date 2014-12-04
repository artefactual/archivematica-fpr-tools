import os.path
import re
import subprocess
import sys

def file_tool(path):
    return subprocess.check_output(['file', path]).strip()

class FidoFailed(Exception):
    def __init__(self, stdout, stderr, retcode):
        message = """ 
Fido exited {retcode} and no format was found.
stdout: {stdout}
---
stderr: {stderr}
""".format(stdout=stdout, stderr=stderr, retcode=retcode)
        super(FidoFailed, self).__init__(message)

def identify(file_):
    # The default buffer size fido uses, 256KB, is too small to be able to detect certain formats
    # Formats like office documents and Adobe Illustrator .ai files will be identified as other, less-specific formats
    # This larger buffer size is a bit slower and consumes more RAM, so some users may wish to customize this to reduce the buffer size
    # See: https://projects.artefactual.com/issues/5941, https://projects.artefactual.com/issues/5731
    cmd = ['fido', '-bufsize', '1048576',
           '-loadformats', '/usr/lib/archivematica/archivematicaCommon/externals/fido/archivematica_format_extensions.xml',
           os.path.abspath(file_)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = process.communicate()

    try:
        results = stdout.split('\n')[0].split(',')
    except:
        raise FidoFailed(stdout, stderr, process.returncode)

    if process.returncode != 0 or results[-1] == '"fail"':
        raise FidoFailed(stdout, stderr, process.returncode)
    else:
        puid = results[2]
        if re.match('(.+)?fmt\/\d+', puid):
            return puid
        else:
            print >> sys.stderr, "File identified as non-standard Fido code: {id}".format(id=puid)
            return "" 

def main(argv):
    try:
        print identify(argv[1])
        return 0
    except FidoFailed as e:
        file_output = file_tool(argv[1])
        # FIDO can't currently identify text files with no extension, and this
        # is a common enough usecase to special-case it
        if 'text' in file_output:
            print 'x-fmt/111'
        else:
            return e
    except Exception as e:
        return e

if __name__ == '__main__':
    exit(main(sys.argv))
