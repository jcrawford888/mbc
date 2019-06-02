import pytest
import mbc
import os

url = "http://www.unmuseum.org/bealepap.htm"

METHOD_FAST = 1
METHOD_FLEX = 2
METHOD_STRICT = 3


def test_version():
    assert mbc.__version__ == "0.1.0"


def test_encrypt_decrypt_file_default(clear_info):
    clear_filename, clear_text = clear_info

    outdata = mbc.encrypt(clear_filename, url)
    outfilename = "mbctest.mbc"
    if os.path.isfile(outfilename):
        # delete the previous output file
        os.unlink(outfilename)
    mbc.write(outfilename, outdata, METHOD_FLEX)

    msg = mbc.decrypt(outfilename, url)

    os.unlink(outfilename)

    assert msg == clear_text


def test_encrypt_decrypt_file_flex(clear_info):
    clear_filename, clear_text = clear_info

    outdata = mbc.encrypt(clear_filename, url, METHOD_FLEX)
    outfilename = "mbctest.mbc"
    if os.path.isfile(outfilename):
        # delete the previous output file
        os.unlink(outfilename)
    mbc.write(outfilename, outdata, METHOD_FLEX)

    msg = mbc.decrypt(outfilename, url)

    os.unlink(outfilename)

    assert msg == clear_text


def test_encrypt_decrypt_file_fast(clear_info):
    clear_filename, clear_text = clear_info

    outdata = mbc.encrypt(clear_filename, url, METHOD_FAST)
    outfilename = "mbctest.mbc"
    if os.path.isfile(outfilename):
        # delete the previous output file
        os.unlink(outfilename)
    mbc.write(outfilename, outdata, METHOD_FAST)

    msg = mbc.decrypt(outfilename, url)

    os.unlink(outfilename)

    assert msg == clear_text.lower()


def test_encrypt_decrypt_file_strict(clear_info):
    clear_filename, clear_text = clear_info

    outdata = mbc.encrypt(clear_filename, url, METHOD_STRICT)
    outfilename = "mbctest.mbc"
    if os.path.isfile(outfilename):
        # delete the previous output file
        os.unlink(outfilename)
    mbc.write(outfilename, outdata, METHOD_STRICT)

    msg = mbc.decrypt(outfilename, url)

    os.unlink(outfilename)

    assert msg == clear_text


def test_encrypt_decrypt_string_default():
    clear_text = "This is a secret message."

    cipher_arr = mbc.encrypts(clear_text, url)

    msg = mbc.decrypts(cipher_arr, url, METHOD_FLEX)

    assert msg == clear_text


def test_encrypt_decrypt_string_flex():
    clear_text = "This is a secret message."

    cipher_arr = mbc.encrypts(clear_text, url, METHOD_FLEX)

    msg = mbc.decrypts(cipher_arr, url, METHOD_FLEX)

    assert msg == clear_text


def test_encrypt_decrypt_string_fast():
    clear_text = "This is a secret message."

    cipher_arr = mbc.encrypts(clear_text, url, METHOD_FAST)

    msg = mbc.decrypts(cipher_arr, url, METHOD_FAST)

    assert msg == clear_text.lower()


def test_encrypt_decrypt_string_strict():
    clear_text = "This is a secret message."

    cipher_arr = mbc.encrypts(clear_text, url, METHOD_STRICT)

    msg = mbc.decrypts(cipher_arr, url, METHOD_STRICT)

    assert msg == clear_text


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
