from glob import glob
import os
import subprocess
import tempfile
import shutil


def burst_pdf(input, output):
    cmd = ["gs", "-o", output, "-sDEVICE=png16m",
           "-r300", "-dPDFFitPage=true", input]
    return subprocess.check_call(cmd)


def ocr_file(input, outname):
    cmd = ["tesseract", input, outname, "pdf"]
    return subprocess.check_call(cmd)


def join_pdfs(inputs, output):
    cmd = ["pdftk"] + inputs + ["cat", "output", output]
    return subprocess.check_call(cmd)


def scale_pdf(input, output):
    cmd = ["gs", "-sDEVICE=pdfwrite",
                 "-sPAPERSIZE=letter",
                 "-dFIXEDMEDIA",
                 "-dPDFFitPage",
                 "-o", output,
                 input]
    return subprocess.check_call(cmd)


def main(input, output):
    try:
        tempdir = tempfile.mkdtemp()

        # Produces individual pages, for OCR via Tesseract
        # Note, this can take a *long* time
        burst_pdf(input, os.path.join(tempdir, "out-%05d.png"))

        for f in glob(os.path.join(tempdir, "*.png")):
            outname = os.path.splitext(f)[0]
            ocr_file(f, outname)

        pdfs = sorted(glob(os.path.join(tempdir, "*.pdf")))
        joined_file = os.path.join(tempdir, "joined.pdf")
        join_pdfs(pdfs, joined_file)

        scale_pdf(joined_file, output)
    finally:
        shutil.rmtree(tempdir)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file-full-name", dest="input")
    parser.add_argument("--output-location", dest="output")
    args, _ = parser.parse_known_args()

    main(args.input, args.output)
