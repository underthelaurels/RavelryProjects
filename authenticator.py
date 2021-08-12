import json
import requests

class Authenticator:
    readOnly = False

    def __init__(self, ro):
        readOnly = ro
        # import the json and store username and password
        with open('config.json') as json_file:
            data = json.load(json_file)
            
            # grab the right user and pass based on the readOnly value
            if readOnly:
                self.username = data['readOnly']['user']
                self.password = data['readOnly']['pass']
            else:
                self.username = data['personal']['user']
                self.password = data['personal']['pass']
        

a = Authenticator(False)
base = 'https://api.ravelry.com'
url = base + '/current_user.json'
response = requests.get(url, auth=(a.username, a.password))
print(response.status_code)