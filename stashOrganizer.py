import json
from types import TracebackType
import requests
from requests.models import Response

class StashOrganizer:

    def __init__(self, info):
        # import the json and store username and password
        with open('config.json') as json_file:
            data = json.load(json_file)
            self.username = data['personal']['user']
            self.password = data['personal']['pass']
            self.person = data['person']

        # fetch all the stash data once
        self.stash = self.fetchStash()
        self.colors = self.fetchColorfams()
        self.weights = self.fetchYarnWeights()

        if info:
            self.prettyDump('stash')
            self.prettyDump('colors')
            self.prettyDump('weights')


    def fetchStash(self):
        #Fetch personal stash data from Ravelry
        url = 'https://api.ravelry.com/people/' + self.person + '/stash/list.json'
        params = {'sort': 'weight'}
        response = requests.get(url, auth=(self.username, self.password), params=params)
        data = response.json()['stash']
        return data

    def fetchColorfams(self):
        # Get the list of color families from Ravelry
        url = 'https://api.ravelry.com/color_families.json'
        response = requests.get(url, auth=(self.username, self.password))
        data = response.json()['color_families']
        return data
    
    def fetchYarnWeights(self):
        # Get the list of yarn weights from Ravelry
        url = 'https://api.ravelry.com/yarn_weights.json'
        response = requests.get(url, auth=(self.username, self.password))
        data = response.json()['yarn_weights']
        return data


    def printBasicStashInfo(self):
        print("Total stash items: ", len(self.stash))
        
        # we countin now
        inStashCount = 0
        usedCount = 0
        giftedCount = 0

        colorCounts = dict()

        for yarn in self.stash:
            if yarn['stash_status']['id'] == 1:
                inStashCount += 1
            elif yarn['stash_status']['id'] == 2:
                usedCount += 1
            elif yarn['stash_status']['id'] == 4:
                giftedCount += 1
            
            if yarn['color_family_name'] in colorCounts:
                colorCounts[yarn['color_family_name']] += 1
            elif yarn['color_family_name'] != None:
                colorCounts[yarn['color_family_name']] = 1

        # printing out the counts
        print("In stash: ", inStashCount)
        print("Used up: ", usedCount)
        print("Gifted: ", giftedCount)
        print("Stash Color Counts:") # Print the stash color counts from most to least frequent
        for color in sorted(colorCounts, key=colorCounts.get, reverse=True):
            print("    ", color, ":", colorCounts[color])


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


org = StashOrganizer(0)
org.printBasicStashInfo()