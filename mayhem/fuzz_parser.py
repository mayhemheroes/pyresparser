#! /usr/bin/env python3
import io
import logging
import sys
import tempfile
import warnings
from zipfile import BadZipFile

import atheris
with atheris.instrument_imports(include=['pyresparser']):
    import pyresparser.utils as utils

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

supported_exts = [
    (".pdf", False),
    (".doc", True),
    (".docx", True)
]


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    #Pick file extension
    ext, requires_file_path = supported_exts[fdp.ConsumeIntInRange(0, len(supported_exts)-1)]

    temp_file = None
    file_data = fdp.ConsumeBytes(atheris.ALL_REMAINING)
    if requires_file_path or fdp.ConsumeBool():
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(file_data)
        temp_file.flush()
        fd = temp_file.name
    else:
        fd = io.BytesIO()
        fd.write(file_data)
        fd.name = "test" + ext

    try:
        utils.get_number_of_pages(fd)
        text = ' '.join(utils.extract_text(fd, ext).split())
        utils.extract_email(text)
        utils.extract_mobile_number(text)
    except BadZipFile:
        pass

    # Clean-up
    if temp_file:
        temp_file.close()


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
