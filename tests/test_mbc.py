import pytest
import mbc
import os

url = "http://www.unmuseum.org/bealepap.htm"


def test_version():
    assert mbc.__version__ == "0.1.0"


def test_encrypt_decrypt_file():
    clear_text = "This is a secret message."
    infile_name = "mbctest_clear.txt"
    fh = open(infile_name, "w")
    fh.write(clear_text)
    fh.close()

    outdata = mbc.encrypt(infile_name, url)
    outfilename = "mbctest.mbc"
    if os.path.isfile(outfilename):
        # delete the previous output file
        os.unlink(outfilename)
    mbc.write(outfilename, outdata)

    msg = mbc.decrypt(outfilename, url)

    os.unlink(infile_name)
    os.unlink(outfilename)

    assert msg == clear_text.lower()


def test_encrypt_decrypt_string():
    clear_text = "This is a secret message."

    cipher_arr = mbc.encrypts(clear_text, url)

    msg = mbc.decrypts(cipher_arr, url)

    assert msg == clear_text.lower()


def test_encrypts_missing_message():
    with pytest.raises(ValueError):
        mbc.encrypts("", url)


def test_encrypts_missing_url():
    with pytest.raises(ValueError):
        mbc.encrypts("Hello World", "")


def test_encrypt_missing_filename():
    with pytest.raises(ValueError):
        mbc.encrypt("", url)


def test_encrypt_missing_url():
    with pytest.raises(ValueError):
        mbc.encrypt("filename.txt", "")


def test_decrypts_missing_arr():
    with pytest.raises(ValueError):
        mbc.decrypts([], url)


def test_decrypts_missing_url():
    with pytest.raises(ValueError):
        mbc.decrypts([0], "")


def test_decrypt_missing_filename():
    with pytest.raises(ValueError):
        mbc.decrypt("", url)


def test_decrypt_missing_url():
    with pytest.raises(ValueError):
        mbc.decrypt("filename.txt", "")
