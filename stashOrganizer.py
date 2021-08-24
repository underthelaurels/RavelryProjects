import json
from os import path
from types import TracebackType
from typing import DefaultDict
import requests

import progressbar

class StashOrganizer:

    def __init__(self, dump, update):
        # import the json and store username and password
        with open('config.json') as jsonFile:
            data = json.load(jsonFile)
            self.username = data['personal']['user']
            self.password = data['personal']['pass']
            self.person = data['person']

        # fetch all the stash data
        self.stash = self.fetchStash(update)
        self.scraps, self.usable = self.getScrapUsableLists()

        if dump:
            self.colors = self.fetchColorfams()
            self.weights = self.fetchYarnWeights()
            self.prettyDump('all')

    ###
    ### Fetch functions for getting Ravelry data
    ### 

    def fetchStash(self, update):
        # Update stash from Ravelry if dump file doesn't exist
        if update or not path.exists('stash_dump.json'):
            print('Getting stash from Ravelry...')
            # Fetch personal stash data from Ravelry
            baseUrl = 'https://api.ravelry.com/people/' + self.person + '/stash/'
            params = {'sort': 'weight'}
            response = requests.get(baseUrl + 'list.json', auth=(self.username, self.password), params=params)
            smallStash = response.json()['stash']

            fullStash = '['
            # Get full stash list
            with progressbar.ProgressBar(max_value=len(smallStash)) as bar:
                for stashItem in smallStash:
                    # Get the stash ID and use it to call API stash/show
                    response = requests.get(baseUrl + str(stashItem['id']) + '.json', auth=(self.username, self.password))
                    fullStash += json.dumps(response.json()['stash']) + ','
                    bar.update(smallStash.index(stashItem))
            
            fullStash = fullStash[:-1] +']'
            return json.loads(fullStash)
        else:
            with open('stash_dump.json') as jsonFile:
                stash = json.load(jsonFile)
            return stash

    def fetchColorfams(self):
        # Only get colors from Ravelry if dump file doesn't exist
        if (path.exists('color_dump.json')):
            with open('color_dump.json') as jsonFile:
                data = json.load(jsonFile)
        else:
            # Get the list of color families from Ravelry
            url = 'https://api.ravelry.com/color_families.json'
            response = requests.get(url, auth=(self.username, self.password))
            data = response.json()['color_families']
        return data
    
    def fetchYarnWeights(self):
        # Only get weights from Ravelry if dump file doesn't exist
        if (path.exists('weight_dump.json')):
            with open('weight_dump.json') as jsonFile:
                data = json.load(jsonFile)
        else:
            # Get the list of yarn weights from Ravelry
            url = 'https://api.ravelry.com/yarn_weights.json'
            response = requests.get(url, auth=(self.username, self.password))
            data = response.json()['yarn_weights']
        return data

    ###
    ### Functions to manipulate and display stash data
    ###

    def calcBasicInfo(self):
        # we countin
        usableCount = 0
        usedCount = 0
        giftedCount = 0
        washableCount = 0

        for stashItem in self.stash:
            itemColor = stashItem['color_family_name']
            itemWeight = stashItem['yarn_weight_name']
            # checking yarn statuses and adding to counts
            if stashItem['stash_status']['id'] == 1 and stashItem in self.usable:
                # counting how many in stash yarns are washable
                if 'yarn' in stashItem and stashItem['yarn']['machine_washable']:
                    washableCount += 1
                usableCount += 1                
            elif stashItem['stash_status']['id'] == 2:
                usedCount += 1
            elif stashItem['stash_status']['id'] == 4:
                giftedCount += 1
                
        
        output = 'Basic Stash Info -'

        # output the stash status counts
        output += '\n\tTotal stash items: ' + str(len(self.stash))
        output += '\n\tUsable: ' + str(usableCount)
        output += '\n\tScraps: ' + str(len(self.scraps))
        output += '\n\tUsed up: ' + str(usedCount)
        output += '\n\tGifted: ' + str(giftedCount)
        output += '\n\tMachine Washable: ' + str(washableCount) + '/' + str(usableCount) + ' yarns'
        
        return output + '\n\n\n'


    def calcUsableAmounts(self):
        colorCounts = DefaultDict(int)
        weightCounts = DefaultDict(int)

        yardTotal = 0
        yardsByWeight = DefaultDict(float)
        yardByColor = DefaultDict(float)

        gramsTotal = 0
        gramsByWeight = DefaultDict(float)
        gramsByColor = DefaultDict(float)

        for stashItem in self.usable:
            itemWeight = stashItem['yarn_weight_name']
            itemColor = stashItem['color_family_name']
            itemGrams = stashItem['packs'][1]['total_grams']
            itemYards = stashItem['packs'][1]['total_yards']

            colorCounts[itemColor] += 1
            weightCounts[itemWeight] += 1

            if itemYards is not None and itemColor is not None:
                yardTotal += itemYards
                yardsByWeight[itemWeight] += itemYards
                yardByColor[itemColor] += itemYards

            if itemGrams is not None and itemColor is not None:
                gramsTotal += itemGrams
                gramsByWeight[itemWeight] += itemGrams
                gramsByColor[itemColor] += itemGrams
        
        # Format for printing/exporting
        output = 'Usable Yarn Amounts -'
        
        output += '\n\tTotal Grams/Yardages: ' + '{:>6.0f} g,{:>6.0f} yds'.format(gramsTotal, yardTotal)
        output += '\n\n\tYarns/Grams/Yardages by Color:'
        for color in sorted(gramsByColor, key=gramsByColor.get, reverse=True):
            s = '\n\t\t{:<14}-{:>4} yarns,{:>6.0f} g,{:>6.0f} yds'
            output += s.format(color, colorCounts[color], gramsByColor[color], yardByColor[color])

        output += '\n\n\tYarns/Grams/Yardages by Weight:'
        for weight in gramsByWeight:
            s = '\n\t\t{:<16}-{:>4} yarns,{:>6.0f} g,{:>6.0f} yds'
            output += s.format(weight, weightCounts[weight], gramsByWeight[weight], yardsByWeight[weight])

        return output + '\n\n\n'

    def getScrapUsableLists(self):
        scrapList = []
        usableList = []
        # return a list of stash items considered 'scraps' (<25g of yarn and In Stash)
        # and return a list of stash items considered 'usable' (>= 25g of yarn and In Stash)
        for stashItem in self.stash:
            #Check if in stash
            if stashItem['stash_status']['id'] == 1:
                # check if < 25g of yarn
                if (stashItem['packs'][1]['total_grams'] is not None and
                        stashItem['packs'][1]['total_yards'] is not None and
                        stashItem['packs'][1]['total_grams'] < 25):
                    scrapList.append(stashItem)
                else:
                    usableList.append(stashItem)
        return scrapList, usableList

    def calcScrapAmounts(self):
        colorCounts = DefaultDict(int)
        weightCounts = DefaultDict(int)

        yardTotals = 0
        yardsByColor = DefaultDict(float)
        yardsByWeight = DefaultDict(float)
        
        for stashItem in self.scraps:
            colorCounts[stashItem['color_family_name']] += 1
            weightCounts[stashItem['yarn_weight_name']] += 1

            itemYards = stashItem['packs'][1]['total_yards']

            yardTotals += itemYards
            yardsByColor[stashItem['color_family_name']] += itemYards
            yardsByWeight[stashItem['yarn_weight_name']] += itemYards
        
        # Format for printing/exporting
        output = 'Scrap Information -'
        output += '\n\tTotal Yardage: {:.1f} yds'.format(yardTotals)
        output += '\n\n\tYardage by Color:'
        for color in sorted(yardsByColor, key=yardsByColor.get, reverse=True):
            output += '\n\t\t{:<14}-{:>8.1f} yds'.format(str(color), yardsByColor[color])
        output += '\n\n\tYardage by Weight:'
        for weight in yardsByWeight:
            output += '\n\t\t{:<16}-{:>8.1f} yds'.format(weight, yardsByWeight[weight])
        
        return output + '\n\n\n'


    def prettyDump(self, type):
        if type == 'stash' or type == 'all':
            with open('stash_dump.json', 'w') as writeFile:
                json.dump(self.stash, writeFile, indent=4)
        elif type == 'colors' or type == 'all':
            with open('color_dump.json', 'w') as writeFile:
                json.dump(self.colors, writeFile, indent=4)
        elif type == 'weights' or type == 'all':
            with open('weight_dump.json', 'w') as writeFile:
                json.dump(self.weights, writeFile, indent=4)