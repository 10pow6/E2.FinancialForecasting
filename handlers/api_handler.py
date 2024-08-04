import json
import os
from statics import DirectoryConfig

class APIHandler:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        self.options={}
    def set_options(self,config_file):
        file_path = DirectoryConfig.configs + "/" + config_file
        print(file_path)

        try:
            with open(file_path, 'r') as file:
                self.options = json.load(file)
        except FileNotFoundError:
            print("The file was not found")
        except json.JSONDecodeError:
            print("The file does not contain valid JSON")
        
        print(self.options)
        
    def V2_tileprices(self,client):
        r = client.get( self.E2_V2_API+"tileprices/",headers=self.headers )
        return r.json()