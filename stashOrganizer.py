import json
from os import path
from types import TracebackType
import requests
from requests.models import Response

class StashOrganizer:

    def __init__(self, info):
        # import the json and store username and password
        with open('config.json') as jsonFile:
            data = json.load(jsonFile)
            self.username = data['personal']['user']
            self.password = data['personal']['pass']
            self.person = data['person']

        # fetch all the stash data
        self.stash = self.fetchStash()

        if info:
            self.colors = self.fetchColorfams()
            self.weights = self.fetchYarnWeights()
            self.prettyDump('stash')
            self.prettyDump('colors')
            self.prettyDump('weights')

    ###
    ### Fetch functions for getting Ravelry data
    ### 

    def fetchStash(self):
        # Only get stash from Ravelry if dump file doesn't exist
        if (path.exists('stash_dump.json')):
            with open('stash_dump.json') as jsonFile:
                data = json.load(jsonFile)
        else:
            # Fetch personal stash data from Ravelry
            url = 'https://api.ravelry.com/people/' + self.person + '/stash/list.json'
            params = {'sort': 'weight'}
            response = requests.get(url, auth=(self.username, self.password), params=params)
            data = response.json()['stash']
        return data

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

    def printBasicStashInfo(self):
        # we countin
        inStashCount = 0
        usedCount = 0
        giftedCount = 0

        colorCounts = dict()
        weightCounts = dict()

        for stashItem in self.stash:
            # counting yarn statuses
            if stashItem['stash_status']['id'] == 1:
                inStashCount += 1
            elif stashItem['stash_status']['id'] == 2:
                usedCount += 1
            elif stashItem['stash_status']['id'] == 4:
                giftedCount += 1
            
            # counting yarns of each color (only if currently in stash)
            if stashItem['stash_status']['id'] == 1:
                if stashItem['color_family_name'] in colorCounts:
                    colorCounts[stashItem['color_family_name']] += 1
                elif stashItem['color_family_name'] != None:
                    colorCounts[stashItem['color_family_name']] = 1

            # counting yarns of each weight (only if currently in stash)
            if 'yarn' in stashItem and stashItem['stash_status']['id'] == 1:
                if stashItem['yarn']['yarn_weight']['name'] in weightCounts:
                    weightCounts[stashItem['yarn']['yarn_weight']['name']] += 1
                else:
                    weightCounts[stashItem['yarn']['yarn_weight']['name']] = 1

        # print the stash status counts
        print('Total stash items:', len(self.stash))
        print('In stash:', inStashCount)
        print('Used up:', usedCount)
        print('Gifted:', giftedCount)

        # print the stash color counts from most to least frequent
        print('\nStash Colors: (in stash only)') 
        for color in sorted(colorCounts, key=colorCounts.get, reverse=True):
            print('    ', color, ':', colorCounts[color])
        
        # print the stash weight counts
        print('\nStash Weights: (in stash only)')
        for weight in weightCounts:
            print('    ', weight, ':', weightCounts[weight])


    def prettyDump(self, type):
        if type == 'stash':
            with open('stash_dump.json', 'w') as writeFile:
                json.dump(self.stash, writeFile, indent=4)
        elif type == 'colors':
            with open('color_dump.json', 'w') as writeFile:
                json.dump(self.colors, writeFile, indent=4)
        elif type == 'weights':
            with open('weight_dump.json', 'w') as writeFile:
                json.dump(self.weights, writeFile, indent=4)


###
### Function calls
###

org = StashOrganizer(0)
org.printBasicStashInfo()