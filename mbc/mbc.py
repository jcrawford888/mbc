#!/usr/bin/python3

"""
Modernized Beale Cipher

This encryption mechanism uses a url link from any website and converts the page to text to use as a 'book'
The message is then encoded as offsets into the converted text.
When used with the corresponding decryption routine and url the book will be converted the same way and the offsets can be used to
convert the cipher back to the original message (clear text).
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


def encrypt(infilename=None, url=None):
    """
    Encrypt the contents of the file specified in the parameters. Use the contents of the url as the 'book' for
    encrypting the contents. NOTE: htmls tags are removed from the book contents and all text is lower-cased.

    :param infilename: file containing the message to encrypt
    :param url: the url pointing to a page of text that will be used as the 'book'
    :return: array of integer offsets into the 'book'
    """
    if not url:
        raise ValueError('Missing url')

    if not infilename:
        raise ValueError('Missing input file')

    fh = open(infilename, 'r')
    lines = []
    for line in fh:
        lines.append(line)

    fh.close()

    message = ' '.join(lines)

    try:
        book = __prepare_book(url)
    except:
        raise

    booklen = len(book)

    offsetmap = {}
    offsets = []
    for ch in message:
        ch = ch.lower()

        encoded = False
        while not encoded:
            # find a random offset in the book then search forward to find the character
            offset = random.randint(0, booklen - 1)

            if ch != book[offset]:
                # hunt forward for a character (loop to beginning if not found)
                # abort if we looped and hit this index again
                offsetorig = offset
                looped = False

                while 1:
                    offset = offset + 1

                    if offset >= booklen:
                        looped = True
                        offset = 0

                    if looped and offset >= offsetorig:
                        # looped once and couldn't find a character in the book to encode the message character, abort
                        raise ValueError(
                            "Couldn't find a character in the book to encode the message character {}. Find a bigger book. Aborting.".format(ch))

                    if ch == book[offset]:
                        # found the character we need
                        break

            # make sure we don't use the same offset more than once in the encoded message
            if offset not in offsetmap:
                encoded = True
                offsetmap[offset] = 1
                offsets.append(offset)

    return offsets


def decrypt(infilename=None, url=None):
    """
    Decrypt a file that has been encoded using mbc.

    :param infilename: The cipher text file encrypted using the encryption routine
    :param url: same url as used by the encryption routine
    :return: string containing the decrypted message
    """
    if not url:
        raise ValueError('Missing url')

    if not infilename:
        raise ValueError('Missing input file')

    if not os.path.isfile(infilename):
        raise ValueError('Unable to open file: {}'.format(infilename))

    fh = open(infilename, 'rb')

    header = pickle.load(fh)
    if not header or header != 'mbc':
        raise ValueError('Invalid mbc cipher file')

    # We may use this later if we have different versions of the output format
    magicnum = pickle.load(fh)

    ciphertext = pickle.load(fh)

    fh.close()

    try:
        book = __prepare_book(url)
    except:
        raise

    booklen = len(book)

    if booklen == 0:
        raise ValueError('Book is empty')

    messagearr = []
    for offset in ciphertext:

        if offset >= booklen or offset < 0:
            raise ValueError(
                'Bad offset ({}).  Out of bounds for this book'.format(offset))

        messagearr.append(book[offset])

    message = ''.join(messagearr)

    return message


def __prepare_book(urllink):
    # try to get the data from the url

    raw = requests.get(urllink)


    handler = html2text.HTML2Text()
    handler.ignore_images = True
    handler.ignore_links = True
    handler.ignore_tables = True

    # extract the text from the url (e.g. 'book')
    clean = handler.handle(raw.text).lower()

    return clean


def write(outfile, data):
    """
    Routine to write out the encrypted data to a file
    convert the ints to a binary format and put a small header in the front. e.g.) mbc

    :param outfile: the name of the file to write the encrypted contents into
    :param data: array of offsets to write (encrypted message)
    :return: None
    """

    if os.path.isfile(outfile):
        raise ValueError('File {} already exists. aborting.'.format(outfile))

    fh = open(outfile, 'wb')

    # write the header
    pickle.dump('mbc', fh)

    # write the magic number
    pickle.dump(MAGIC, fh)

    # write the data
    pickle.dump(data, fh)

    fh.close()
