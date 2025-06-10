#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Copyright (c) 2025 Sayan Ray
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# Redistribution of this file, in source or binary form, with or without
# modification, is permitted provided that the above notice is retained.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------------

from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType

def check_args():
	parser = ArgumentParser(description = "bcHunt - An autonomous badchar finder.", usage = "bcHunt.py <sequence file> -b [badchars]", formatter_class = RawDescriptionHelpFormatter, epilog = """Examples:
  bcHunt.py seq.bin			# Finds the first occurence of a badchar.

  bcHunt.py seq.bin -b \"\\x0a\\xaf\\xb2\"	# Finds the next occurence of a badchar.
""")

	parser.add_argument("sequence", metavar = "Sequence File", help = "The dumped binary file containing the user's input; basically the ESP dump.", type = FileType('rb'))
	parser.add_argument("-b", "--badchars", metavar = "", help = "List of previously found badchars.")

	return parser.parse_args()

def compare(sequence, raw, badchars):
	# Remove the badchars from the list of all the chars if there is any supplied badchars
	for x in badchars:
		raw.pop(raw.index(x))

	success = 0

	# Loop through the sequence
	for i in range(0, len(sequence)):

		# if the byte in sequence doesn't match with the pre-defined sequence, and the byte from the pre-defined sequence itself isn't a mentioned badchar, then the byte from the given sequence is a badchar
		if sequence[i] != raw[i] and raw[i] not in badchars:
			print("[*] Badchar found: \\x{:02x}".format(raw[i]))
			print("[*] Removing it ...")
			print("[+] New payload :")
			badchars.append(raw[i])

			# Print the badchar removed list of chars, for further testing
			for x in range(1, 256):
				if x not in badchars:
					print("\\x{:02x}".format(x), end="")

			success = 0
			print()
			break
		success = 1

	if success:
		print("[+] No Badchars found!!")

if __name__ == '__main__':
	args = check_args()

	# Generate a list of all the chars
	raw = bytearray(bytes(range(1, 256)))

	# Read the sequence file
	sequence = bytearray(args.sequence.read())

	# Remove the null byte, if the user passes any
	args.badchars = args.badchars.replace("\\x00", "") if args.badchars and "\\00" in args.badchars else args.badchars

	# Convert string '\\x0a' to byte '\x0a' and then make a bytearray out of them
	badchars = bytearray(args.badchars.encode('latin-1').decode('unicode_escape').encode('latin-1') if args.badchars else b"")

	# Compare them
	compare(sequence, raw, badchars)