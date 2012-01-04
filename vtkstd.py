#!/usr/bin/env python2
import fileinput, glob, string, sys, os, re

# Build up a list of all export macros to replace.
pattern = re.compile("#include <vtkstd/")
patterna = re.compile("#include \"vtkstd/")
pattern2 = re.compile("vtkstd::")

def searchReplace(path):
  files = glob.glob(path)
  if files is not []:
    for file in files:
      if os.path.isfile(file):
        for line in fileinput.input(file, inplace=1):
          lineNumber = pattern.search(line)
          if lineNumber >= 0:
            #print "Found a line to replace: " + line
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

#searchReplace("*/*.txx")
#searchReplace("*/*.cxx")
#searchReplace("*/*.h*")
#searchReplace("*/*.py")
#searchReplace("*/Testing/Cxx/*.cxx")
#searchReplace("*/Testing/Cxx/*.h")
#searchReplace("Utilities/*/*.cxx")
#searchReplace("Utilities/*/*.h*")
#searchReplace("Wrapping/*/*.cxx")
#searchReplace("Examples/*/Cxx/*.cxx")
#searchReplace("Examples/*/Cxx/*.h")
#searchReplace("GUISupport/Qt/*.h")
#searchReplace("GUISupport/Qt/*.cxx")

searchReplace("Applications/ParaView/*.cxx")
searchReplace("Applications/ParaView/*.h*")
searchReplace("CMake/*")
searchReplace("CommandLineExecutables/*")
searchReplace("CoProcessing/*/*")
searchReplace("Common/*/*")
searchReplace("ParaView*/*/*")
searchReplace("ParaView*/*/*/*")
searchReplace("ParaView*/*/*/*/*")
searchReplace("CoProcessing/CoProcessor/Testing/TestDriver/*")
searchReplace("Examples/Plugins/*/*")
searchReplace("Plugins/*/*")
searchReplace("Plugins/*/*/*")
searchReplace("Plugins/*/*/*/*htop")