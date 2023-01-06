import json
from os import path
from typing import DefaultDict
import requests
import progressbar

'''
    This class imports and processes stash data from Ravelry
'''
class StashOrganizer:
    def __init__(self, dump, update):
        # import the config file and store username and password
        with open('config.json') as jsonFile:
            data = json.load(jsonFile)
            self.username = data['personal']['user']
            self.password = data['personal']['pass']
            self.person = data['person']

        # fetch all the stash data from Ravelry or a json file
        self.stash = self.fetchStash(update)
        # seperate the scraps from the rest of the stash (ie, main stash)
        self.scraps, self.main = self.getScrapMainLists()

        # Output raw ravelry stash data, color families, and yarn weights to json files
        if dump:
            self.colors = self.fetchColorfams()
            self.weights = self.fetchYarnWeights()
            self.prettyDump('all')
        elif update:
            print("Updating raw Ravelry stash json...")
            self.prettyDump('stash')

    '''
        Fetch functions for getting Ravelry data
    '''
    def fetchStash(self, update):
        # Update stash from Ravelry if dump file doesn't exist
        if update or not path.exists('stash_dump.json'):
            print('Getting stash from Ravelry...')
            # Send GET request to Ravelry for small stash list
            baseUrl = 'https://api.ravelry.com/people/' + self.person + '/stash/'
            params = {'sort': 'weight'}
            response = requests.get(
                baseUrl + 'list.json', auth=(self.username, self.password), params=params)
            smallStash = response.json()['stash']

            fullStash = '['
            # Get full stash list using the IDs from the small stash list
            # Show the user a progress bar to help with the wait
            with progressbar.ProgressBar(max_value=len(smallStash)) as bar:
                for stashItem in smallStash:
                    # Get the stash ID and use it to call GET stash/show on API
                    response = requests.get(
                        baseUrl + str(stashItem['id']) + '.json', auth=(self.username, self.password))
                    fullStash += json.dumps(response.json()['stash']) + ','
                    bar.update(smallStash.index(stashItem))

            fullStash = fullStash[:-1] + ']'
            # Load the resulting stash list and return it
            return json.loads(fullStash)
        else:
            # Skip calling to Ravelry and pull data from dump file instead
            with open('stash_dump.json') as jsonFile:
                stash = json.load(jsonFile)
            return stash

    def fetchColorfams(self):
        # Only get colors family list from Ravelry if dump file doesn't exist
        if (path.exists('color_dump.json')):
            with open('color_dump.json') as jsonFile:
                data = json.load(jsonFile)
            return data
        else:
            # GET the list of color families from Ravelry
            url = 'https://api.ravelry.com/color_families.json'
            response = requests.get(url, auth=(self.username, self.password))
            return response.json()['color_families']

    def fetchYarnWeights(self):
        # Only get weights from Ravelry if dump file doesn't exist
        if (path.exists('weight_dump.json')):
            with open('weight_dump.json') as jsonFile:
                return json.load(jsonFile)
        else:
            # GET the list of yarn weights from Ravelry
            url = 'https://api.ravelry.com/yarn_weights.json'
            response = requests.get(url, auth=(self.username, self.password))
            return response.json()['yarn_weights']

    '''
        Counts generic stash stuff and returns a list of info
    '''
    def calcBasicInfo(self):
        # we countin
        mainCount = 0
        usedCount = 0
        giftedCount = 0
        washableCount = 0

        for stashItem in self.stash:
            # checking yarn statuses and adding to counts
            if stashItem['stash_status']['id'] == 1 and stashItem in self.main:
                # counting how many in stash yarns are washable
                if 'yarn' in stashItem and stashItem['yarn']['machine_washable']:
                    washableCount += 1
                mainCount += 1
            elif stashItem['stash_status']['id'] == 2:
                usedCount += 1
            elif stashItem['stash_status']['id'] == 4:
                giftedCount += 1

        info = [
            len(self.stash),
            mainCount,
            len(self.scraps),
            usedCount,
            giftedCount,
            washableCount
        ]
        return info

    '''
        Calculates yardage, grams, and stash item counts for
        each yarn material type located in the main stash.
        Returns a list of information
    '''
    def calcMaterialInfo(self):
        pass
        # TODO implement
    
    '''
        Calculates stash item counts for each type of yarn
        care (if available) located in the main stash.
        Returns a dictionary of {yarn care type : stash item count}
    '''
    def calcWashableInfo(self):
        pass
        # TODO implement

    '''
        Calculates yardage, grams and stash item counts for
        each color family and yarn weight located in the main or scrap stash.
        Returns a list of information
    '''
    def calcAmounts(self, type):
        if type == 'main':
            type = self.main
        else:
            type = self.scraps
        colorCounts = DefaultDict(int)
        weightCounts = DefaultDict(int)

        yardTotal = 0
        yardsByColor = DefaultDict(float)
        yardsByWeight = DefaultDict(float)

        gramsTotal = 0
        gramsByColor = DefaultDict(float)
        gramsByWeight = DefaultDict(float)

        for stashItem in type:
            itemColor = stashItem['color_family_name']
            itemWeight = stashItem['yarn_weight_name']
            itemGrams = stashItem['packs'][1]['total_grams']
            itemYards = stashItem['packs'][1]['total_yards']

            colorCounts[str(itemColor)] += 1
            weightCounts[itemWeight] += 1

            if itemYards is not None:
                yardTotal += itemYards
                yardsByColor[str(itemColor)] += itemYards
                yardsByWeight[itemWeight] += itemYards

            if itemGrams is not None:
                gramsTotal += itemGrams
                gramsByColor[str(itemColor)] += itemGrams
                gramsByWeight[itemWeight] += itemGrams

        amounts = [
            colorCounts,
            weightCounts,
            yardTotal,
            yardsByColor,
            yardsByWeight,
            gramsTotal,
            gramsByColor,
            gramsByWeight
        ]
        return amounts

    '''
        Returns 2 lists of stash items - one of the stash scraps and
        one of the main stash
    '''
    def getScrapMainLists(self):
        scrapList = []
        mainList = []
        # return a list of stash items considered 'scraps' (taggged 'scraps or <40g of yarn and In Stash)
        # and return a list of stash items considered 'non-scrap' or 'main' yarn (tagged 'usable' or >= 40g of yarn and In Stash)
        for stashItem in self.stash:
            # Check if listed as in stash
            if stashItem['stash_status']['id'] == 1:
                # check if item is tagged with 'usable' or 'scraps'
                #print(stashItem['tag_names'])
                if ('usable' in stashItem['tag_names']):
                    mainList.append(stashItem)
                elif ('scraps' in stashItem['tag_names']):
                    scrapList.append(stashItem)
                # otherwise check if less than 40g of yarn
                else:
                    if (stashItem['packs'][1]['total_grams'] is not None and
                            stashItem['packs'][1]['total_yards'] is not None and
                            stashItem['packs'][1]['total_grams'] < 40):
                        scrapList.append(stashItem)
                    else:
                        mainList.append(stashItem)
        return scrapList, mainList

    '''
        Helper to dump stored Ravelry data to json files
        Useful when running the script multiple times, since
        storing the data locally is faster than calling the Ravelry API 
    '''
    def prettyDump(self, type):
        if type == 'stash' or type == 'all':
            with open('stash_dump.json', 'w') as writeFile:
                json.dump(self.stash, writeFile, indent=4)
            print("Output raw Ravelry stash data to 'stash_dump.json'\n")
        if type == 'colors' or type == 'all':
            with open('color_dump.json', 'w') as writeFile:
                json.dump(self.colors, writeFile, indent=4)
            print("Output raw Ravelry color family data to 'color_dump.json'\n")
        if type == 'weights' or type == 'all':
            with open('weight_dump.json', 'w') as writeFile:
                json.dump(self.weights, writeFile, indent=4)
            print("Output raw Ravelry yarn weight data to 'weight_dump.json'\n")
