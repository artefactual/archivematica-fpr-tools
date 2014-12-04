import json
import subprocess
import sys

from lxml import etree

class JhoveException(Exception):
    pass

def parse_jhove_data(target):
    args = ['jhove', '-h', 'xml', target]
    try:
        output = subprocess.check_output(args)
    except subprocess.CalledProcessError:
        raise JhoveException("Jhove failed when running: " + ' '.join(args))

    return etree.fromstring(output)

def get_status(doc):
    status = doc.find('.{http://hul.harvard.edu/ois/xml/ns/jhove}repInfo/{http://hul.harvard.edu/ois/xml/ns/jhove}status')
    if status is None:
        raise JhoveException("Unable to find status!")

    return status.text

def get_outcome(status, format=None):
    # JHOVE returns "bytestream" for unrecognized file formats.
    # That can include unrecognized or malformed PDFs, JPEG2000s, etc.
    # Since we're whitelisting the formats we're passing in,
    # "bytestream" indicates that the format is not in fact well-formed
    # regardless of what the status reads.
    if format == "bytestream":
        return "fail"

    if status == "Well-Formed and valid":
        return "pass" 
    elif status == "Well-Formed, but not valid":
        return "partial pass" 
    else:
        return "fail" 

def get_format(doc):
    format = doc.find('.{http://hul.harvard.edu/ois/xml/ns/jhove}repInfo/{http://hul.harvard.edu/ois/xml/ns/jhove}format')
    version = doc.find('.{http://hul.harvard.edu/ois/xml/ns/jhove}repInfo/{http://hul.harvard.edu/ois/xml/ns/jhove}version')

    if format is None:
        format = "Not detected" 
    else:
        format = format.text

    if version is not None:
        version = version.text

    return (format, version)

def format_event_outcome_detail_note(format, version, result):
    note = 'format="{}";'.format(format)
    if version is not None:
        note = note + ' version="{}";'.format(version)
    note = note + ' result="{}"'.format(result)

    return note

def main(target):
    try:
        doc = parse_jhove_data(target)
        status = get_status(doc)
        format, version = get_format(doc)
        outcome = get_outcome(status, format)
        note = format_event_outcome_detail_note(format, version, status)

        out = {
            "eventOutcomeInformation": outcome,
            "eventOutcomeDetailNote": note
        }
        print json.dumps(out)

        return 0
    except JhoveException as e:
        return e

if __name__ == '__main__':
    target = sys.argv[1]
    sys.exit(main(target))
