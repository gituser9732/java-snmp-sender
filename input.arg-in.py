#!/bin/python
#
#
import sys, getopt

def main(argv):

   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv, "a:r:" ,["account", "region"])

   except getopt.GetoptError:
      print("test.py -a <account> -r <region>")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print("test.py -a <account> -r <region>")
         sys.exit()
      elif opt in ("-a", "--account"):
         inputfile = arg
      elif opt in ("-r", "--region"):
         outputfile = arg
   print('Account is: {}'.format(inputfile))
   print('Region is: {}'.format(outputfile))

if __name__ == "__main__":
   main(sys.argv[1:])
