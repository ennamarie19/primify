#!/usr/bin/env python3
import atheris
import contextlib
import sys
import io
import traceback
from PIL import Image

with atheris.instrument_imports(exclude=['sympy*']):
    from primify.base import PrimeImage


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout


@atheris.instrument_func
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    
    f = io.BytesIO(data)
    f.seek(0)

    try:
        image = Image.open(f)
        with nostdout():
            quant_img = PrimeImage.quantize_image(image)
            PrimeImage.quantized_image_to_number(quant_img)
    except Exception as e:
        if 'PIL' in traceback.format_exc():
            return -1
        raise



def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
