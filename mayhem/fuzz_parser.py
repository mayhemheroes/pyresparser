#! /usr/bin/python3
import io
import logging
import sys
from zipfile import BadZipFile

import atheris
import warnings

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

with atheris.instrument_imports():
    import pdfminer
    import docx2txt

import pyresparser.utils as utils

supported_exts = [".pdf", ".doc", ".docx"]


@atheris.instrument_func
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    #Pick file extension
    ext = supported_exts[fdp.ConsumeIntInRange(0, len(supported_exts)-1)]
    fd = io.BytesIO()
    fd.name = "test" + ext
    fd.write(fdp.ConsumeBytes(atheris.ALL_REMAINING))

    try:
        utils.get_number_of_pages(fd)
        text = ' '.join(utils.extract_text(fd, ext).split())
        utils.extract_email(text)
        utils.extract_mobile_number(text)
    except BadZipFile:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
