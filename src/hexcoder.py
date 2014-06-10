#! /usr/bin/env python

from __future__ import print_function

import sys

__version__ = 'v1.0.0'
__authors__ = 'Damian Jason Lapidge <grey@greydamian.org>'
__license__ = '''Copyright (c) Damian Jason Lapidge

The contents of this file are subject to the terms and conditions defined 
within the file LICENSE.txt, located within this project's root directory.
'''

BUFSIZE = 32 # must be multiple of 32, so beautify works correctly

HEXCHARS = '0123456789ABCDEFabcdef'

ENCODE   = 0
DECODE   = 1
BEAUTIFY = 2

def print_usage():
    print('usage: hexcoder-py [-e] [-d] [-b]', file=sys.stderr)

def parse_args(args):
    opts = {'mode': ENCODE}

    for s in args:
        if s == '-e':
            opts['mode'] = ENCODE
        elif s == '-d':
            opts['mode'] = DECODE
        elif s == '-b':
            opts['mode'] = BEAUTIFY

    return opts

def read(f, size):
    return f.read(size)

def readhex(f, size):
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

def main(args):
    try:
        opts = parse_args(args)
    except ValueError:
        print_usage()
        return 1 # failure

    read_func = read
    if opts['mode'] == BEAUTIFY or opts['mode'] == DECODE:
        read_func = readhex

    buf = read_func(sys.stdin, BUFSIZE)
    while buf != '':
        if opts['mode'] == ENCODE:
            buf = buf.encode('hex').upper()
        if opts['mode'] == BEAUTIFY or opts['mode'] == ENCODE:
            buf = beautify(buf)
        if opts['mode'] == DECODE:
            if len(buf) % 2 != 0:
                buf = buf[:-1]
            buf = buf.decode('hex')

        sys.stdout.write(buf)
        buf = read_func(sys.stdin, BUFSIZE)

    return 0 # success

if __name__ == '__main__':
    sys.exit(main(sys.argv))

