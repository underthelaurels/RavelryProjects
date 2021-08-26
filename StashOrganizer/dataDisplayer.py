import matplotlib.pyplot as plt
import numpy
import matplotlib.backends.backend_pdf
import pandas


labelcolors = {
    'Yellow': 'xkcd:yellow',
    'Yellow-orange': 'xkcd:goldenrod',
    'Orange': 'xkcd:orange',
    'Red-orange': 'xkcd:orangered',
    'Red': 'xkcd:red',
    'Red-purple': 'mediumvioletred',
    'Purple': 'xkcd:purple',
    'Blue-purple': 'mediumslateblue',
    'Blue': 'xkcd:blue',
    'Blue-green': 'xkcd:aqua',
    'Green': 'xkcd:green',
    'Yellow-green': 'xkcd:yellowgreen',
    'Black': 'xkcd:black',
    'White': 'xkcd:ivory',
    'Gray': 'xkcd:grey',
    'Brown': 'xkcd:brown',
    'Pink': 'xkcd:pink',
    'Natural/Undyed': 'xkcd:beige',
    'Multicolored': 'xkcd:tan',
    'Rainbow\t': 'xkcd:chartreuse',
    'None': 'xkcd:silver',
    'Other': 'xkcd:coral'
}

'''
    Formats input data into a return string
    Data includes stash item counts for each stash status type
    as well as machine washable data
'''
def formatBasicData(self, data):
    # format the data
    output = 'Basic Stash Info -'
    output += '\n\tTotal stash items: {}'.format(data[0])  # Total
    output += '\n\tMain: {}'.format(data[1])  # Main yarn
    output += '\n\tScraps: {}'.format(data[2])  # Scraps
    output += '\n\tUsed up: {}'.format(data[3])  # Used Up
    output += '\n\tGifted: {}'.format(data[4])  # Gifted
    # Washable
    output += '\n\tMachine Washable: {}/{} yarns'.format(data[5], data[1])
    output += '\n\n\n'

    return output

'''
    Formats input data into a return string.
    Data includes yardage, grams, colors, weight, and stash item amounts
    for the main stash. The main stash is made up of stash items containing
    more than 25 grams of yarn.
'''
def formatMainData(self, data):
    # pull everything out of data and name it all nice
    colorCounts = data[0]
    weightCounts = data[1]
    yardTotal = data[2]
    yardsByColor = data[3]
    yardsByWeight = data[4]
    gramsTotal = data[5]
    gramsByColor = data[6]
    gramsByWeight = data[7]

    # Format for printing/exporting
    output = 'Main Yarn Amounts -'
    output += '\n\tTotal Grams/Yardage: ' + \
        '{:>6.0f} g,{:>6.0f} yds'.format(gramsTotal, yardTotal)

    output += '\n\n\tYarns/Grams/Yardage by Color:'
    for color in sorted(gramsByColor, key=gramsByColor.get, reverse=True):
        s = '\n\t\t{:<14}-{:>4} yarns,{:>6.0f} g,{:>6.0f} yds'
        output += s.format(color, colorCounts[color],
                            gramsByColor[color], yardsByColor[color])

    output += '\n\n\tYarns/Grams/Yardage by Weight:'
    for weight in gramsByWeight:
        s = '\n\t\t{:<16}-{:>4} yarns,{:>6.0f} g,{:>6.0f} yds'
        output += s.format(weight, weightCounts[weight],
                            gramsByWeight[weight], yardsByWeight[weight])

    output += '\n\n\n'
    return output

'''
    Formats input data into a return string.
    Data includes yardage, colors, weight, and stash item amounts
    for stash scraps. Stash scraps are made up of stash items containing
    less than 25 grams of yarn.
'''
def formatScrapData(self, data):
    colorCounts = data[0]
    weightCounts = data[1]
    yardTotals = data[2]
    yardsByColor = data[3]
    yardsByWeight = data[4]

    # Format for printing/exporting
    output = 'Scrap Information -'
    output += '\n\tTotal Yardage: {:.1f} yds'.format(yardTotals)

    output += '\n\n\tYarns/Yardage by Color:'
    for color in sorted(yardsByColor, key=yardsByColor.get, reverse=True):
        s = '\n\t\t{:<14}-{:>4} yarns,{:>8.1f} yds'
        output += s.format(str(color),
                            colorCounts[color], yardsByColor[color])

    output += '\n\n\tYarns/Yardage by Weight:'
    for weight in yardsByWeight:
        s = '\n\t\t{:<16}-{:>4} yarns,{:>8.1f} yds'
        output += s.format(weight,
                            weightCounts[weight], yardsByWeight[weight])

    output += '\n\n\n'
    return output

'''
    Creates and returns 1 bar graph and 1 pie chart
    based on given basic yarn data. 
    barGraph    - a horizontal bar chart plotting stash item counts for each stash status type
        the main 4 stash stash status types are [Main, Scraps, Used Up, Gifted]
    pieChart    - a pie chart representing makeup of machine washable yarns in the main stash
'''
def chartBasicData(self, data):
    # Bar graph: main, scraps, used up, gifted
    barGraph = plt.figure(1)
    heights = data[1:-1]
    names = "Main", "Scraps", "Used Up", "Gifted"
    yPos = numpy.arange(len(names))
    # Create the bars
    plot = plt.barh(yPos, heights, color=[
                    'tab:green', 'tab:orange', 'tab:red', 'tab:blue'])
    plt.gca().invert_yaxis()
    plt.bar_label(plot, labels=heights, padding=3)
    # Create graph labels
    plt.title('Basic Stash Data')
    plt.yticks(yPos, names)
    plt.xlabel('Number of Stash Items')

    # Pie chart: machine washable percentage
    pieChart = plt.figure(2)
    plt.pie([data[-1], data[0]-data[-1]], labels=('Machine Washable', 'Not'), autopct='%1.0f%%',
            radius=1.2, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    plt.title('Machine Washable Yarns', y=1.05)
    plt.axis('off')

    return barGraph, pieChart

'''
    Creates and returns 2 pie charts and 2 bar charts
    based on main stash data. The main stash is made up of stash items containing
    more than 25 grams of yarn.
    pieColor    - a pie chart representing the color makeup of the main stash
    pieWeight   - a pie chart representing the yarn weight makeup of the main stash
    barColor    - a horizontal bar chart plotting gram amounts for each color group
    barWeight   - a horizontal bar chart plotting gram amounts for each yarn weight
'''
def chartMainData(self, data):
    # pull everything out of data and name it all nice
    colorCounts = data[0]
    gramsByColor = data[6]
    gramsByWeight = data[7]

    #
    # Pie chart 1: yarn % by color
    #
    pieColor = plt.figure(3)
    total = sum(colorCounts.values())
    labels = []
    col = []
    values = []
    other = 0
    for color in sorted(colorCounts, key=colorCounts.get, reverse=True):
        # If the color percent is greater than 4%, add it normally to the pie chart
        if colorCounts[color] / total > 0.04:
            labels.append(color)
            col.append(self.labelcolors[color])
            values.append(colorCounts[color])
        else:
            other += colorCounts[color]
    # if the other count exists, add other to the chart
    if other > 0:
        labels.append('Other')
        col.append(self.labelcolors['Other'])
        values.append(other)

    plt.pie(values, labels=labels, labeldistance=1.05, colors=col, radius=1.2, autopct='%1.0f%%',
            pctdistance=0.85, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    plt.title("Main Stash by Yarn Color", y=1.05)

    #
    # Pie Chart 2: yarn % by weight in grams
    #
    pieWeight = plt.figure(4)

    weightColors = self.makePrettyColors(gramsByWeight)
    plt.pie(gramsByWeight.values(), labels=gramsByWeight.keys(), colors=weightColors, labeldistance=1.05,
            radius=1.2, autopct='%1.0f%%', pctdistance=0.85, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    plt.title("Main Stash by Yarn Weight", y=1.05)

    #
    # Bar chart 1: colors broken up by grams
    #
    barColor = plt.figure(5)
    plt.title("Main Stash Yarn Colors in Grams")
    height = []
    names = []
    col = []
    for color in self.labelcolors.keys():
        if gramsByColor[color] > 0:
            height.append(gramsByColor[color])
            names.append(color)
            col.append(self.labelcolors[color])
    yPos = numpy.arange(len(names))
    plt.barh(yPos, height, color=col)
    plt.gca().invert_yaxis()
    plt.yticks(yPos, names)
    plt.subplots_adjust(left=0.18)
    plt.xlabel('Grams')

    #
    # Bar chart 2: weights broken up by grams
    #
    barWeight = plt.figure(6)
    plt.title("Main Stash Yarn Weights in Grams")
    names = gramsByWeight.keys()
    height = gramsByWeight.values()
    yPos = numpy.arange(len(names))
    plt.barh(yPos, height, color=weightColors)
    plt.gca().invert_yaxis()
    plt.yticks(yPos, names)
    plt.subplots_adjust(left=0.18)
    plt.xlabel('Grams')

    return pieColor, pieWeight, barColor, barWeight

'''
    Creates and returns 2 bar charts based on stash scraps data. Stash scraps are
    made up of stash items containing less than 25 grams of yarn.
    barColor    - a horizontal bar chart plotting scrap yardages for each color group
    barWeight   - a horizontal bar chart plotting scrap yardages for each yarn weight
'''
def chartScrapData(self, data):
    yardsByColor = data[3]
    yardsByWeight = data[4]

    # Bar chart 1: colors by yardage
    barColor = plt.figure(7)
    plt.title("Scrap Yarn Colors")
    height = []
    names = []
    col = []
    for color in self.labelcolors.keys():
        if yardsByColor[color] > 0:
            height.append(yardsByColor[color])
            names.append(color)
            col.append(self.labelcolors[color])
    yPos = numpy.arange(len(names))
    plt.barh(yPos, height, color=col)
    plt.gca().invert_yaxis()
    plt.yticks(yPos, names)
    plt.subplots_adjust(left=0.18)
    plt.xlabel('Yards')

    # Bar chart 2: weights by yardage
    barWeight = plt.figure(8)
    plt.title("Scrap Yarn Weights")
    weightColors = self.makePrettyColors(yardsByWeight)
    names = yardsByWeight.keys()
    height = yardsByWeight.values()
    yPos = numpy.arange(len(names))
    plt.barh(yPos, height, color=weightColors)
    plt.gca().invert_yaxis()
    plt.yticks(yPos, names)
    plt.subplots_adjust(left=0.18)
    plt.xlabel('Yards')

    return barColor, barWeight

'''
    Helper to create a list of colors from a gradient to be used
    in a chart. Returns a list of colors
'''
def makePrettyColors(self, weightData):
    weightColors = []
    map = plt.get_cmap('viridis', len(weightData.keys()))
    for x in range(len(weightData.keys()) - 1, -1, -1):
        weightColors.append(map(x / len(weightData.keys())))
    return weightColors

'''
    Creates a text file of formatted data based on the data parameters "basic, main, scrap"
    data are chosen to be formatted and printed by the parameter "type"
    Prints to command line upon completion
'''
def outputTextToFile(self, type, basic, main, scrap):
    with open('Stash_Output.txt', 'w') as writeFile:
        if type in {'basic', 'b', 'all', 'a'}:
            writeFile.write(self.formatBasicData(basic))
        if type in {'main', 'm', 'all', 'a'}:
            writeFile.write(self.formatMainData(main))
        if type in {'scrap', 's', 'all', 'a'}:
            writeFile.write(self.formatScrapData(scrap))
    print("Wrote stash information to 'Stash_Output.txt'\n")

'''
    Creates a pdf of charts based on the data parameters "basic, main, scrap"
    Charts are chosen to be printed by the parameter "type"
    Prints to command line upon completion
'''
def outputChartsToFile(self, type, basic, main, scrap):
    with matplotlib.backends.backend_pdf.PdfPages("Stash_Output.pdf") as pdf:
        if type in {'basic', 'b', 'all', 'a'}:
            basicBar, basicPie = self.chartBasicData(basic)
            pdf.savefig(basicBar)
            pdf.savefig(basicPie)
        if type in {'main', 'm', 'all', 'a'}:
            mainPieColor, mainPieWeight, mainBarColor, mainBarWeight = self.chartMainData(
                main)
            pdf.savefig(mainPieColor)
            pdf.savefig(mainPieWeight)
            pdf.savefig(mainBarColor)
            pdf.savefig(mainBarWeight)
        if type in {'scrap', 's', 'all', 'a'}:
            scrapBarColor, scrapBarWeight = self.chartScrapData(scrap)
            pdf.savefig(scrapBarColor)
            pdf.savefig(scrapBarWeight)
    print("Saved stash charts to 'Stash_Output.pdf'\n")
