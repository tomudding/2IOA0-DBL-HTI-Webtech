"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-04
"""
import csv

def generateRadialGraph(file, directed):
    if directed == False or directed == None:
        return generateUndirectedRadialGraph(file)
    else:
        return generateDirectedRadialGraph(file)

def generateDirectedRadialGraph(file):
    return ""

def generateUndirectedRadialGraph(file):
    return ""

##############################################################################
# THESE FUNCTIONS SHOULD PROBABLY BE IN A SEPARATE FILE FOR DATA AGGREGATION #
##############################################################################
def processCSVFile(file):
    for row in getCSVData(file):
        return ""

# Get header from CSV file row by row
def getCSVHeader(file):
    with open(file, 'rb') as csvfile:
        header = csvfile.readline()
    return header

# Get data from CSV file row by row
# This improves memory management
# and runtime for larger files
def getCSVData(file):
    with open(file, 'rb') as csvfile:
        line = csvfile.readline()                   # get first line
        dialect = csv.Sniffer().sniff(line)         # sniff dialect of CSV file (delimiter etc.)
        csvfile.seek(0)                             # return pointer to BOF (beginning of file)
        datareader = csv.reader(csvfile, dialect)   # create CSV reader with sniffed dialect
        header = next(datareader)                   # skip header of file
        for row in datareader:
            yield row