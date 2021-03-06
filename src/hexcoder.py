#! /usr/bin/env python

from __future__ import print_function

import sys
import getopt

__version__ = 'v1.0.0'
__authors__ = 'Damian Jason Lapidge <grey@greydamian.org>'
__license__ = '''Copyright (c) 2015 Damian Jason Lapidge

The contents of this file are subject to the terms and conditions defined 
within the file LICENSE.txt, located within this project's root directory.
'''

BUFSIZE = 32 # must be multiple of 32, so beautify works correctly

HEXCHARS = '0123456789ABCDEFabcdef'

# modes of operation
ENCODE   = 0
DECODE   = 1
BEAUTIFY = 2

def print_usage():
    """Prints command usage information to stderr."""
    print('usage: hexcoder-py [-e] [-d] [-b]', file=sys.stderr)

def parse_args(args):
    """Parses the user supplied command line arguments.

    Args:
        args: List of strings corresponding to supplied command line arguments.

    Returns:
        A tuple of 2 dictionaries. The first dictionary represents command 
        options, the second dictionary represents required command arguments.

    Raises:
        ValueError: A supplied command option is not recognised.
    """
    optstr = 'edb'

    try:
        opts, args = getopt.getopt(args[1:], optstr)
    except getopt.GetoptError:
        raise ValueError('unrecognised option')

    # result dicts
    cmdargs = {}
    cmdopts = {'mode': ENCODE}

    for opt, arg in opts:
        if opt in ('-e'):
            cmdopts['mode'] = ENCODE
        elif opt in ('-d'):
            cmdopts['mode'] = DECODE
        elif opt in ('-b'):
            cmdopts['mode'] = BEAUTIFY

    return cmdopts, cmdargs

def read(f, size):
    """Reads bytes from a file.

    Args:
        f:    File object from which to read data.
        size: Maximum number of bytes to be read from file.

    Returns:
        String of bytes read from file.
    """
    return f.read(size)

def readhex(f, size):
    """Reads only hexadecimal characters from a file.

    Any non-hexadecimal characters are ignored and omitted from the returned 
    string.

    Args:
        f:    File object from which to read data.
        size: Maximum number of characters to be read from file.

    Returns:
        String of hexadecimal characters read from file.
    """
    result = ''

    while len(result) < size:
        c = f.read(1)

        if c == '':
            break # end of file reached

        if not c in HEXCHARS:
            continue # skip non-hex chars

        result += c

    return result

def beautify(s):
    """Formats a hexadecimal string to make it more easily readable.

    The hexadecimal string is made more easily readable by inserting additional 
    whitespace characters.

    Args:
        s: Hexadecimal string to be formatted.

    Returns:
        Formatted string.
    """
    result = ''

    for i in xrange(len(s)):
        result += s[i]

        if i + 1 >= len(s):
            result += '\n'
            continue

        if (i + 1) % 2 == 0:
            result += ' ' # append space

        if (i + 1) % 32 == 0:
            result = result[:-1] + '\n' # replace space with newline
        elif (i + 1) % 8 == 0:
            result += ' ' # append second space

    return result

def main(args=None):
    """Program entry point."""
    try:
        cmdopts, cmdargs = parse_args(args)
    except ValueError as e:
        print_usage()
        return 1 # failure

    read_func = read
    if cmdopts['mode'] == BEAUTIFY or cmdopts['mode'] == DECODE:
        read_func = readhex

    buf = read_func(sys.stdin, BUFSIZE)
    while buf != '':
        if cmdopts['mode'] == ENCODE:
            buf = buf.encode('hex').upper()
        if cmdopts['mode'] == BEAUTIFY or cmdopts['mode'] == ENCODE:
            buf = beautify(buf)
        if cmdopts['mode'] == DECODE:
            if len(buf) % 2 != 0:
                buf = buf[:-1]
            buf = buf.decode('hex')

        sys.stdout.write(buf)
        buf = read_func(sys.stdin, BUFSIZE)

    return 0 # success

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        # handle SIGINT
        sys.exit(1) # failure
    except Exception:
        # handle all Exception, but not BaseException, subclasses
        print('error: unhandled exception', file=sys.stderr)
        sys.exit(1) # failure

