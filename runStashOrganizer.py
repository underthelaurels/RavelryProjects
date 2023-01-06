import argparse
from StashOrganizer import stashOrganizer, dataDisplayer

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
                    help='''the output type for the data - 
                    text file output - [text, t]. chart pdf output - [chart, charts, c]. 
                    both file output types - [both, b, all]''')

args = parser.parse_args()

org = stashOrganizer.StashOrganizer(args.dump, args.update)
basic = org.calcBasicInfo()
main = org.calcAmounts('main')
scrap = org.calcAmounts('scrap')

if args.output_type in {'text', 't'}:
    # Sends data to output as a text file
    dataDisplayer.outputTextToFile(args.info_type, basic, main, scrap)
elif args.output_type in {'chart', 'charts', 'c'}:
    # Sends data to output as a chart pdf
    dataDisplayer.outputChartsToFile(args.info_type, basic, main, scrap)
elif args.output_type in {'both', 'b', 'all'}:
    # Sends data to output as both a text file and a chart pdf
    dataDisplayer.outputTextToFile(args.info_type, basic, main, scrap)
    dataDisplayer.outputChartsToFile(args.info_type, basic, main, scrap)