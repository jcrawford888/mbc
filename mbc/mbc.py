#!/usr/bin/python3

"""
Modernized Beale Cipher

This encryption mechanism uses a url link from any website and converts the page to text to use as a 'book'
The message is then encoded as offsets into the converted text.
When used with the corresponding decryption routine and url the book will be converted the same way and the offsets can
be used to convert the cipher back to the original message (clear text).
Prior to using the technique the two parties should agree on a method to determine the book (url) to use.  e.g.) send
a hint in an email such as 'I saw a great article on cats yesterday'. Recipient can find news articles from yesterday
about cats and try each link until the message decodes.  Probably send the hint by a different delivery method. e.g.)
email the ciphertext and 'text' the hint.
"""

import requests
import html2text
import random
import os
import pickle

# Just a magic number to distinguish different formats
MAGIC = 0x1

# Encryption methods
# FAST - all characters lower cased
# FLEX - attempts to find a capital Letter in book, otherwise uses lower case. (default)
# STRICT - Match the message exactly, fails if can't find capitals
METHOD_FAST = 1
METHOD_FLEX = 2
METHOD_STRICT = 3


def encrypts(message=None, url=None, method=METHOD_FLEX):
    """
    Encrypt the message string specified in the parameters. Use the contents of the url as the 'book' for
    encrypting the contents. NOTE: html tags are removed from the book contents and all text is lower-cased.

    :param message: parameter containing the message to encrypt
    :param url: the url pointing to a page of text that will be used as the 'book'
    :param method: encryption method
    :return: array of integer offsets into the 'book'
    """

    if not message:
        raise ValueError("Missing message to encrypt")

    if not url:
        raise ValueError("Missing url")

    try:
        book = _prepare_book(url, method)
    except Exception:
        raise

    def _encode_char(ch, book):
        while True:
            # find a random offset in the book then search forward to find the character
            offset = random.randint(0, len(book) - 1)

            if ch != book[offset]:
                # hunt forward for a character (loop to beginning if not found)
                # abort if we looped and hit this index again
                offsetorig = offset
                looped = False

                while True:
                    offset = offset + 1

                    if offset >= len(book):
                        looped = True
                        offset = 0

                    if looped and offset >= offsetorig:
                        # looped once and couldn't find a character in the book to encode the message character, abort
                        return -1

                    if ch == book[offset]:
                        # found the character we need
                        break

            # make sure we don't use the same offset more than once in the encoded message
            if offset not in offsetmap:
                return offset

    offsetmap = {}
    offsets = []
    for ch in message:
        if method == METHOD_FAST:
            ch = ch.lower()

        offset = _encode_char(ch, book)
        if offset < 0 and method == METHOD_FLEX:
            # try again with lower cased char
            offset = _encode_char(ch.lower(), book)

        if offset < 0:
            raise ValueError(
                f"Could not find a character in the book to encode the message character '{ch}'."
            )

        offsetmap[offset] = 1
        offsets.append(offset)

    return offsets


def encrypt(infilename=None, url=None, method=METHOD_FLEX):
    """
    Encrypt the contents of the file specified in the parameters. Use the contents of the url as the 'book' for
    encrypting the contents. NOTE: html tags are removed from the book contents and all text is lower-cased.

    :param infilename: file containing the message to encrypt
    :param url: the url pointing to a page of text that will be used as the 'book'
    :param method: encryption method
    :return: array of integer offsets into the 'book'
    """
    if not url:
        raise ValueError("Missing url")

    if not infilename:
        raise ValueError("Missing input file")

    fh = open(infilename, "r")
    lines = []
    for line in fh:
        lines.append(line)

    fh.close()

    message = " ".join(lines)

    return encrypts(message, url, method)


def decrypts(cipher_arr=None, url=None, method=METHOD_FLEX):
    """
    Decrypt an array of cipher offsets that has been encoded using mbc.

    :param cipher_arr: The cipher array encrypted using the encryption routine
    :param url: same url as used by the encryption routine
    :return: string containing the decrypted message
    """
    if not url:
        raise ValueError("Missing url")

    if not cipher_arr:
        raise ValueError("Missing cipher array")

    try:
        book = _prepare_book(url, method)
    except Exception:
        raise

    if len(book) == 0:
        raise ValueError("Book is empty")

    message_arr = []
    for offset in cipher_arr:

        if offset >= len(book) or offset < 0:
            raise ValueError(f"Bad offset ({offset}).  Out of bounds for this book")

        message_arr.append(book[offset])

    message = "".join(message_arr)

    return message


def decrypt(infilename=None, url=None):
    """
    Decrypt a file that has been encoded using mbc.

    :param infilename: The cipher text file encrypted using the encryption routine
    :param url: same url as used by the encryption routine
    :return: string containing the decrypted message
    """
    if not url:
        raise ValueError("Missing url")

    if not infilename:
        raise ValueError("Missing input file")

    if not os.path.isfile(infilename):
        raise ValueError(f"Unable to open file: {infilename}")

    with open(infilename, "rb") as fh:
        header = pickle.load(fh)
        if not header or header != "mbc":
            raise ValueError("Invalid mbc cipher file")

        # We may use this later if we have different versions of the output format
        magicnum = pickle.load(fh)

        if magicnum != MAGIC:
            raise ValueError("Bad Magic Number")

        # Get the encryption method used to encrypt the file
        method = pickle.load(fh)

        # load the cipher text offsets
        cipher_arr = pickle.load(fh)

    return decrypts(cipher_arr, url, method)


def _prepare_book(url_link, method=METHOD_FLEX):
    # try to get the data from the url

    raw = requests.get(url_link)

    handler = html2text.HTML2Text()
    handler.ignore_images = True
    handler.ignore_links = True
    handler.ignore_tables = True

    # extract the text from the url (e.g. 'book')
    if method == METHOD_FAST:
        clean = handler.handle(raw.text).lower()
    else:
        clean = handler.handle(raw.text)

    return clean


def write(outfile, data, method=METHOD_FLEX):
    """
    Routine to write out the encrypted data to a file
    convert the ints to a binary format and put a small header in the front. e.g.) mbc

    :param outfile: the name of the file to write the encrypted contents into
    :param data: array of offsets to write (encrypted message)
    :param method: algorithm identifier (e.g fast, flex, strict)
    :return: None
    """

    if os.path.isfile(outfile):
        raise ValueError(f"File {outfile} already exists. aborting.")

    fh = open(outfile, "wb")

    # write the header
    pickle.dump("mbc", fh)

    # write the magic number
    pickle.dump(MAGIC, fh)

    # write the algorithm id used to encrypt the data
    pickle.dump(method, fh)

    # write the data
    pickle.dump(data, fh)

    fh.close()
