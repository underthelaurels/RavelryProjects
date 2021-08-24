import argparse
from stashOrganizer import *

parser = argparse.ArgumentParser(description="Outputs stash information from a logged in user to a file ('Stash_Output.py'). Default is outputting all information.")

parser.add_argument("-f", "--fetch", action="store_true", help="fetch and update stash data from Ravelry")
parser.add_argument("-d", "--dump", action="store_true", help="dump all stash data to json files in pretty json format")
parser.add_argument("-b", "--basic", action="store_true", help="output basic information about your stash")
parser.add_argument("-u", "--usable", action="store_true", help="output 'usable' yarn information (all yarn in stash over 25g)")
parser.add_argument("-s", "--scrap", action="store_true", help="output 'scrap' yarn information (all yarn in stash under 25g)")
parser.add_argument("-a", "--all", action="store_true", help="output all available stash information")


args = parser.parse_args()

dump = False
update = False

if args.dump:
    dump = args.dump
if args.fetch:
    update = args.fetch

org = StashOrganizer(dump, update)

with open('Stash_Output.txt', 'w') as writeFile:
    writeFile.write(str(org.person + '\'s Stash\n').upper())
    writeFile.write('\n(Note: SCRAP items are leftover bits of yarn with less than 25 grams left,\n'
                    '\t USABLE items are yarns with more than 25 grams in stash)\n\n\n')
    
    if args.basic:
        writeFile.write(org.calcBasicInfo())
    if args.usable:
        writeFile.write(org.calcUsableAmounts())
    if args.scrap:
        writeFile.write(org.calcScrapAmounts())
    if args.all or not (args.basic and args.usable and args.scrap):
        writeFile.write(org.calcBasicInfo())
        writeFile.write(org.calcUsableAmounts())
        writeFile.write(org.calcScrapAmounts())

# org = StashOrganizer(1)
# with open('Stash_Output.txt', 'w') as writeFile:
#     writeFile.write(str(org.person + '\'s Stash\n').upper())
#     writeFile.write('\n(Note: SCRAP items are leftover bits of yarn with less than 25 grams left,\n'
#                    '\t USABLE items are yarns with more than 25 grams in stash)\n\n\n')
#     writeFile.write(org.calcBasicInfo())
#     writeFile.write(org.calcUsableAmounts())
#     writeFile.write(org.calcScrapAmounts())

# arguments - 
# --help    :   gives list of arguments
# --update  :   updates stash data from Ravelry
# -dump     :   dumps all stash data to json files in pretty json format
# -basic    :   outputs basic information about your stash
# -usable   :   outputs 'usable' yarn information (all yarn in stash over 25g)
# -scraps   :   outputs 'scrap' yarn information (all yarn in stash under 25g)
# -all      :   output all available stash information