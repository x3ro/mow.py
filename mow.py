#!/usr/bin/env python -u

import subprocess
import time
import sys
import argparse

epilog = """Some usage examples for mow.py:

	mow.py -mr	# Process modified files recursively
	mow.py -r	# Process all files recursively
	mow.py 		# Process files in the current directory
	mow.py -p README.txt test.cpp # Process the specified two files
"""


parser = argparse.ArgumentParser(description='Remove trailing whitespaces from source files', epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--paths', '-p', dest='paths', nargs='+',
					help='Specify files or file-wildcards to be processed. If not specified, the default wildcards will be used.')

parser.add_argument('--recursive', '-r', dest='recursive', action='store_true',
					help='Recursive mode. Git support only works in recursive mode right now!')

parser.add_argument('--force-find', '-f', dest='forceFind', action='store_true',
					help='Force finding files using the "find" command')

parser.add_argument('--only-modified', '-m', dest='onlyModified', action='store_true',
					help='When in Git-mode, process only files that have been modified. Implies recursive mode.')

parser.add_argument('--list-wildcards', '-l', dest='listWildcards', action='store_true',
					help='List source file wildcards which are used to search for files to process')

parser.add_argument('--debug', dest='debug', action='store_true',
					help='Enable debug mode')

args = parser.parse_args()


# We want to process files with the following extensions
sourceFileWildcards = [ '*.java', '*.rb', '*.php', '*.js', '*.scala', '*.c', '*.cpp']

if args.listWildcards:
	print "Wildcards:"
	for wildcard in sourceFileWildcards:
		print "    %s" % wildcard
	exit()

# Ignore subprocess output as explained here:
# http://mail.python.org/pipermail/python-dev/2006-June/066111.html
FNULL = open('/dev/null', 'w')

# Are we currently in a directory under Git version control?
# http://stackoverflow.com/a/2044677/124257
gitRevParse = subprocess.Popen(["git", "rev-parse"], stdout=FNULL, stderr=FNULL)
gitRevParse.wait()
inGitDir = gitRevParse.returncode == 0


# Decide what we want to process. If no path was given, use our wildcards
pathsToProcess = sourceFileWildcards
if args.paths != None:
	pathsToProcess = args.paths


listFileCommand = [ ]

if (args.recursive or args.onlyModified) and inGitDir and not args.forceFind and args.paths == None:
	print "Git mode :)"

	if not args.recursive:
		print "git ls-files does not support non-recursive mode :( Please use -f or -r"
		exit()

	listFileCommand.extend([ "git", "ls-files" ])

	if args.onlyModified:
		listFileCommand.append('--modified')

	for wildcard in pathsToProcess:
		listFileCommand.append( "%s" % wildcard )


elif args.forceFind or args.recursive or args.paths == None:
	print "Find mode."

	if args.onlyModified:
		print "Not in a Git repository, so I cannot process only modified files"
		exit()

	listFileCommand.extend([ "find", ".", "-type", "f" ])

	if not args.recursive:
		listFileCommand.extend(['-depth', '1'])

	listFileCommand.append('(')
	for wildcard in pathsToProcess:
		listFileCommand.extend( ["-name", "%s" % wildcard, '-or'] )

	listFileCommand.pop() # Remove the dangling "-or" at the end
	listFileCommand.append(')')



else:
	listFileCommand.extend(['echo'])

	for wildcard in pathsToProcess:
		listFileCommand.extend( [ wildcard, "\n"] )

	listFileCommand.pop() # Remove the dangling newline at the end


if args.debug:
	print "Arguments parsed:"
	print args
	print "Paths being processed:"
	print pathsToProcess
	print "List File Command:"
	print listFileCommand
	print ""

else:
	sys.stdout.write("Removing trailing spaces.")



files = subprocess.Popen(listFileCommand, stdout=subprocess.PIPE)

# Don't remove the empty argument after -i as Mac OS X doesn't allow -i without parameter
# http://blog.mpdaugherty.com/2010/05/27/difference-with-sed-in-place-editing-on-mac-os-x-vs-linux/
sed = None
if(args.debug):
	print "Data that would be passed to sed:"
	sed = subprocess.Popen([ 'cat' ], stdin=files.stdout)
else:
	sed = subprocess.Popen([ 'xargs', 'sed', '-i', '', '-e', 's/[[:space:]]*$//' ], stdin=files.stdout, stdout=FNULL)
files.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.

if args.debug:
	sed.wait()
	exit()

sed.poll()
while sed.returncode == None:
	sys.stdout.write('.')
	sed.poll()
	time.sleep(0.25)

print ' Done!'
