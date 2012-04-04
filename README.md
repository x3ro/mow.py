# Mow.py

Mow.py is a small python script that shall assist you in your quest to achieve
trailing-space-free code.


# Installation

Clone the repository (or download it), and put mow.py somewhere in your path. If you're
using git, you probably want to put `git-mow` there too :)


# Examples

Some usage examples for mow.py:

	mow.py -r	# Process all files matching the predefined wildcards in the current and all sub-directories
	mow.py 		# Process all files matching the predefined wildcards in the current directory
	mow.py -f README.txt test.cpp	# Process the specified two files

If you installed the git command, you can also do the following:

	git mow		# Process all modified files matching the predefined wildcards
	git mow -m	# Process all files matching the predefined wildcards
	git mow -w \*.pl -w \*.mmd # Process all files matching the predefine wildcards and *.pl and *.mmd


# Bugs and improvements

If you find a bug or have an idea on how to improve Mow.py, please create an issue here on GitHub.


# Boring legal stuff

	Copyright (c) 2012 Lucas Jenß
	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

