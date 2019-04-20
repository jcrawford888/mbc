import mbc
import os


def test_version():
    assert mbc.__version__ == "0.1.0"


def test_encrypt_decrypt():
    cleartext = "This is a secret message."
    infilename = "mbctest_clear.txt"
    fh = open(infilename, "w")
    fh.write(cleartext)
    fh.close()

    url = "http://www.unmuseum.org/bealepap.htm"

    outdata = mbc.encrypt(infilename, url)
    outfilename = "mbctest.mbc"
    if os.path.isfile(outfilename):
        # delete the previous output file
        os.unlink(outfilename)
    mbc.write(outfilename, outdata)

    msg = mbc.decrypt(outfilename, url)

    os.unlink(infilename)
    os.unlink(outfilename)

    assert msg == cleartext.lower()
