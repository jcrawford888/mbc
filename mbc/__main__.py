#!/usr/bin/python3

import mbc
import getopt
import sys


def usage():
    print("Encrypt: mbc -e -f <clear text file> -u <url> -o <output filename>")
    print("Decrypt: mbc -d -f <cipher text file> -u <url> [-o <output filename>]")


def write_clear(outfilename, data):
    # routine to write out the clear text message to a file
    if outfilename:
        fh = open(outfilename, "w")
        for line in data:
            fh.write(line)
        fh.close()
    else:
        print("".join(data))


# get options
opts = []
args = []
try:
    opts, args = getopt.getopt(sys.argv[1:], "hedf:u:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)

outfilename = None
mode = None
infilename = None
url = None
if len(opts) > 0:
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit(0)
        elif opt == "-d":
            if mode is not None:
                print("ERROR: conflicting encrypt/decrypt options")
                usage()
                sys.exit(2)
            mode = "d"
        elif opt == "-e":
            if mode is not None:
                print("ERROR: conflicting encrypt/decrypt options")
                usage()
                sys.exit(2)
            mode = "e"
        elif opt == "-f":
            infilename = arg
        elif opt == "-u":
            url = arg
        elif opt == "-o":
            outfilename = arg

if mode is None:
    print("ERROR: Missing encrypt/decrypt option")
    usage()
    sys.exit(2)

if infilename is None:
    print("ERROR: Missing input filename")
    usage()
    sys.exit(2)

if url is None:
    print("ERROR: Missing url")
    usage()
    sys.exit(2)

if mode == "e" and outfilename is None:
    print("ERROR: outfilename is required for encryption")
    usage()
    sys.exit(2)

outdata = None
if mode == "e":
    # encryption mode, the infile is clear text
    outdata = mbc.encrypt(infilename, url)
    mbc.write(outfilename, outdata)
elif mode == "d":
    outdata = mbc.decrypt(infilename, url)
    write_clear(outfilename, outdata)

print("All Done!")
