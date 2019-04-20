# Modernized Beale Cipher

mbc

I built this tool just for fun.  You can share messages with your friends.  I can't guarantee the security of your messages
so use at your own risk.


## How it works

This encryption mechanism uses a url link from any website and converts the page to text to use as a 'book'
The message is then encoded as offsets into the converted text.

When used with the same url and decryption routine the book will be converted the same way and the offsets can be used to
convert the cipher back to the original message (clear text).

Prior to using the technique the two parties should agree on a method to determine the book (url) to use.  e.g.) send
a hint in an email such as 'I saw a great article on cats yesterday'. Recipient can find news articles from yesterday
about cats and try each link until the message decodes.  Probably send the hint by a different delivery method. e.g.)
email the ciphertext and 'text' the hint


For best results choose a url containing a large amount of text such as a news article, online book etc.

## Usage


python3 -m mbc --help for options


### Encrypting a message

Generate Cipher text from a message

    >>> import mbc
    >>> message = 'Hello World!'
    >>> url = 'https://[url of your choice]'
    >>> cipherdata = mbc.encrypt(message, url)

Now write it out to a file

    >>> mbc.write('secret.mbc', cipherdata)

### Decrypting a message

    >>> msg = mbc.decrypt('secret.mbc', url)
    >>> print(msg)

