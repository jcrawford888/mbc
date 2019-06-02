import pytest
import os

@pytest.fixture(scope="function")
def clear_info():
    clear_text = "This is a secret message."
    infile_name = "mbctest_clear.txt"
    fh = open(infile_name, "w")
    fh.write(clear_text)
    fh.close()

    yield infile_name, clear_text

    os.unlink(infile_name)

