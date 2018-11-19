import sys
import os
import getopt
import logging
import PatternParser
import utilities
import SliceParser
import Matcher
import platform

# Clearing the commandline
clear = "clear"
if platform.system() == "Windows":
    clear = "cls"
os.system(str(clear))

message = """
 Welcome to PHPScan 
 ==================
"""
print(message)


logging.basicConfig(level=logging.WARNING)


def main(argv):

    inputfile = ''

    try:
        opts, _ = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        logging.error('PHPScanner.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logging.info('PHPScanner.py -i <inputfile>')
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            logging.debug('Input file is %s' % inputfile)

    patParser = PatternParser.PatternParser('Patterns')

    patParser.parseAll()

    patterns = patParser.getKnownPatterns()

    entryPoints = utilities.getEntries(patterns)
    validation = utilities.getVals(patterns)
    sensitiveSinks = utilities.getSinks(patterns)

    slic = SliceParser.fileParser(
        inputfile, entryPoints, validation, sensitiveSinks)

    patt = Matcher.match(slic, patterns)

    utilities.printResults(slic, patt)


main(sys.argv[1:])
