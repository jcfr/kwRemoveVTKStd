#!/usr/bin/env python
import fileinput, glob, string, sys, os, re, argparse

# Build up a list of all export macros to replace.
pattern = re.compile("#include <vtkstd/")
patterna = re.compile("#include \"vtkstd/")
pattern2 = re.compile("vtkstd::")

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
      if(verbose):
        print "cleaning: ", f
      replaceFile(fullpath)

def replaceFile(fname):
  for line in fileinput.input(fname, inplace=1):
    lineNumber = pattern.search(line)
    if lineNumber >= 0:
      line = pattern.sub("#include <", line)
      line = line.rstrip() + "\n"
    lineNumber = patterna.search(line)
    if lineNumber >= 0:
      line = patterna.sub("#include \"", line)
      line = line.rstrip() + "\n"
    lineNumber = pattern2.search(line)
    if lineNumber >= 0:
      line = pattern2.sub("std::", line)
      line = line.rstrip() + "\n"
    sys.stdout.write(line)


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
