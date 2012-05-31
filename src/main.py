#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1337 Translator - Translates English text to 1337.
# Copyright (C) 2012 Vinny Diehl
#
# This application is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this application.  If not, see <http://www.gnu.org/licenses/>.

from argparse import ArgumentParser
from json import loads
from pyperclip import copy, paste
from random import choice
from re import findall, sub

### Initialization

opt = ArgumentParser(description='Translate English to 1337.')

# It can only take input from one place, so make these mutually exclusive.
# If no input is selected, it will default to taking input from the keyboard.
input_options = opt.add_mutually_exclusive_group()
input_options.add_argument('-c', '--clipboard', action='store_true',
                            help='Take input from the clipboard.')
input_options.add_argument('-f', '--file',
                            help='Take input from a file.')

# It can output to more than one place, so allow multiple output options.
output_options = opt.add_argument_group('Output', '''Select where to output
                                         the translated text.''')
output_options.add_argument('-C', '--out-clipboard', action='store_true',
                             help='Set the translated text to the clipboard.')
output_options.add_argument('-o', '--output', metavar='FILE',
                             help='Select a file to output the translation to.')

# Add options for fake letters and/or words
fake_options = opt.add_argument_group('Fakeouts', '''Make your text harder to
                                       be read by outsiders.''')
fake_options.add_argument('-l', '--fake-letters', type=int, metavar='INTERVAL',
                           help='Add in a phoney letter at an interval.')
fake_options.add_argument('-w', '--fake-words', type=int, metavar='INTERVAL',
                           help='Add in a phoney word at an interval.')
fake_options.add_argument('-s', '--full-stop', action='store_true',
                           help="Translate '.' to STOP, as in a telegraph.")

# This is useful if they're parsing a big file, outputting the translation
# to another file, and don't want the whole thing thrown in their face.
opt.add_argument('-q', '--quiet', '--silent', action='store_true',
                  help='Suppress all text output to the console.')

opt.add_argument('-t', '--no-trim', '--no-strip', action='store_true',
                 help='Do not trim leading/trailing whitespace from input.')

# Parse all of the arguments to args.
args = opt.parse_args()

# Read in alphabet from JSON file. The alphabet is a dictionary, with each
# (lower case) letter of the English alphabet being a key. The value of each
# key is a list containing all of the possible translation of that letter.
leetalpha = loads(open('alphabet.json').read())

### Input

if args.clipboard:
    # Get a string from the user's clipboard using Pyperclip
    raw = paste()
elif args.file:
    raw = open(args.file).read()
else:
    raw = raw_input('Enter the string to be translated: ')
    print

# We don't want to do pointless translations.
if not raw.strip():
    print 'There is no text to translate in the input data.'
    exit(1)

### Preprocessor

# Get rid of leading/trailing whitespace.
if not args.no_trim:
    raw = raw.strip()

# Show the data that has been read in.
if not args.quiet:
    print 'Original input:\n\n' + raw + '\n'

if args.fake_words:
    # Read in our list of possible words
    words = open('fakewords.txt').read().split('\n')

    # :KLUDGE: 2012-05-31 gbchaosmaster - Regex doesn't capture the last word
    # I tried everything and can't get this to work. I thought about just
    # having a second regex capture the last word but that'd just be sloppy.
    # For now, extremely hacky solution to get the part that the regex missed.
    tokens = findall(r'.+?[\s\n]+(?=[\w(])', raw)
    tokens.append(raw[len(''.join(tokens)):])

    # Stuff for counting and appending:
    i, fake = 0, ''
    for token in tokens:
        if i % args.fake_words == 0 and i > 0:
            fake += choice(words) + ' '
        fake += token
        i += 1

    # Update raw to reflect the changes
    raw = fake

    if not args.quiet:
        print 'String after fake word preprocessing:\n\n' + raw + '\n'

if args.full_stop:
    raw = sub(r' ?\. ?', r' STOP ', raw)

    if not args.quiet:
        print 'String after full stop preprocessing:\n\n' + raw + '\n'

if args.fake_letters:
    # Put in a random character from engalpha every interval. We'll have to
    # count them manually. Same deal as above:
    i, fake = 0, ''
    for ch in raw:
        if ch.isalpha():
            if i % args.fake_letters == 0 and i > 0:
                # Pop in a random letter
                fake += choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            # Only increment if it's a letter, symbols aren't counted.
            i += 1
        fake += ch

    raw = fake

    if not args.quiet:
        print 'String after fake letters preprocessing:\n\n' + raw + '\n'

# Lower case everything to prepare for translation.
raw = raw.lower()

### Translator

# Translate the entire string into 1337 by iterating over each character
# and translating that character only if it is in the English alphabet.
output = ''.join(choice(leetalpha[ch]) if ch.isalpha() else ch for ch in raw)

### Output

if args.out_clipboard:
    # Set the output to the clipboard using Pyperclip.
    copy(output)
elif args.output:
    # Write the output to the specified file.
    open(args.output, 'w').write(output.encode('utf-8'))

if not args.quiet:
    print 'Translated text:\n\n' + output + '\n'
