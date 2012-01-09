#!/usr/bin/env python
import fileinput, glob, string, sys, os, re, argparse

# Build up a list of all vtkstd strings to replace.
patterns = [re.compile("#include <vtkstd/"),\
            re.compile("#include \"vtkstd/"),\
            re.compile("vtkstd::"), \
            re.compile("using namespace vtkstd;")]

# Build up a list of all replacement strings
replacements = ["#include <", "#include \"", "std::", "using namespace std;"]


#parse the file and replace all occurances of vtkstd with std
def replaceFile(fname):
  replacedLine = False
  for line in fileinput.input(fname, inplace=1):
    for pattern,replacement in zip(patterns,replacements):
      lineNumber = pattern.search(line)
      if lineNumber >= 0:
        line = pattern.sub(replacement, line)
        #remove any trailing whitespace at the same time and add back in the
        #new line character
        line = line.rstrip() + "\n"
        replacedLine = True
    sys.stdout.write(line)
  return replacedLine

def dirwalk(dirPath,recurse,ignore):
  "walk a directory tree, using a generator"
  for f in os.listdir(dirPath):
    fullpath = os.path.join(dirPath,f)
    if(recurse and\
       os.path.isdir(fullpath) and\
       not os.path.islink(fullpath) and\
       not f.startswith('.') and\
       not f in ignore):
      for x in dirwalk(fullpath,recurse,ignore):
        yield x
  yield dirPath

#clean all the files in a directory
def cleanDirectory(dirPath,verbose):
  if(verbose):
    print "cleaning directory: ", dirPath

  for f in os.listdir(dirPath):
    fullpath = os.path.join(dirPath,f)
    if(os.path.isfile(fullpath) and\
       not os.path.islink(fullpath) and\
       not f.startswith('.')):
      replaced = replaceFile(fullpath)
      if(verbose and replaced):
        print "removed vtkstd from: ", f



def main():
  parser = argparse.ArgumentParser(description='Remove vtkstd usage from a repository.')
  parser.add_argument('-d', '--directory',
                     required=True,
                     help='root directory to parse')
  parser.add_argument('-i', '--ignore',
                      nargs='+',
                      help='directory to ignore when recursing')
  parser.add_argument('-R', '--recurse',
                      action='store_true',
                      help='recurse the root directory')
  parser.add_argument('-v', '--verbose',
                      action='store_true',
                      help='verbose output')

  args = parser.parse_args()

  #make sure args is an empty list instead of none
  if (args.ignore is None):
    args.ignore = []

  for dirPath in dirwalk(args.directory,args.recurse,args.ignore):
    cleanDirectory(dirPath,args.verbose)

if __name__ == '__main__':
  main()
