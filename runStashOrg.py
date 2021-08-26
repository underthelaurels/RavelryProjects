import argparse
from stashOrganizer import *
from dataDisplayer import *

parser = argparse.ArgumentParser(
    description='''Outputs stash information from a logged in user to a text file
    ('Stash_Output.txt') or to a chart file ('Stash_Output.pdf').
    Default is outputting all information types to a text file.'''
)

# Argument declarations for the Command Line Interface
parser.add_argument("-u", "--update", action="store_true",
                    default=False, help="update stash data from Ravelry")
parser.add_argument("-d", "--dump", action="store_true", default=False,
                    help='''dump all stash data to json files in pretty json format''')
parser.add_argument("info_type", default="all", nargs='?',
                    help='''The type of stash info to output. Can either be 
                    "basic"/"b", "scrap"/"s", "main"/"m", or "all"/"a". 
                    "basic" outputs basic info about your stash. 
                    "scrap" outputs info about yarn in stash under 25g. 
                    "main" outputs info about yarn over 25g. 
                    "all" outputs all info about your stash.''')
parser.add_argument("output_type", default="text", nargs='?',
                    help='''the output type for the data - can either be "text" or "chart". 
                    Can also be shortened to "t" or "c"''')

args = parser.parse_args()

org = StashOrganizer(args.dump, args.update)
disp = DataDisplayer()

# Sends data to output as a text file
if args.output_type == 'text' or args.output_type == 't':
    basic = org.calcBasicInfo()
    main = org.calcMainAmounts()
    scrap = org.calcScrapAmounts()
    disp.outputTextToFile(args.info_type, basic, main, scrap)
# Sends data to output as a chart pdf
elif args.output_type == 'chart' or args.output_type == 'charts' or args.output_type == 'c':
    basic = org.calcBasicInfo()
    main = org.calcMainAmounts()
    scrap = org.calcScrapAmounts()
    disp.outputChartsToFile(args.info_type, basic, main, scrap)
