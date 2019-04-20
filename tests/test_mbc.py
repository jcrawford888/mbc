import mbc
import os


def test_version():
    assert mbc.__version__ == "0.1.0"


def test_encrypt_decrypt_file():
    clear_text = "This is a secret message."
    infile_name = "mbctest_clear.txt"
    fh = open(infile_name, "w")
    fh.write(clear_text)
    fh.close()

    url = "http://www.unmuseum.org/bealepap.htm"

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
    url = "http://www.unmuseum.org/bealepap.htm"

    cipher_arr = mbc.encrypts(clear_text, url)

    msg = mbc.decrypts(cipher_arr, url)

    assert msg == clear_text.lower()
