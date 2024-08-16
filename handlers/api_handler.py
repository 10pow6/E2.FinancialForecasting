import json
import httpx
from statics import DirectoryConfig
import functools
import random
import asyncio
from helpers import lng_lat_to_quadkey_compress
import numpy as np

def async_retry_with_backoff(max_retries, max_backoff, backoff_factor, product_call=False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            backoff = 1
            for _ in range(max_retries):
                try:
                    return await func(self, *args, **kwargs)
                except (httpx.HTTPError, httpx.RequestError) as e:
                    print(f"Error: {e}")
                    if backoff < max_backoff:
                        sleep_time = backoff + random.uniform(0, backoff_factor * backoff)
                        print(f"Retrying in {sleep_time:.2f} seconds...")
                        await asyncio.sleep(sleep_time)
                        backoff *= 2
                    else:
                        if not product_call:
                            print("Maximum backoff reached. Aborting.")
                            raise e
                        else:
                            print("Maximum backoff reached.")
                            return {}  # Empty response for product calls
            
            if not product_call:
                raise Exception("Maximum retries exceeded.")
            else:
                print("Maximum retries exceeded.")
                return {}  # Empty response for product calls
        
        return wrapper
    return decorator


class APIHandler:
    def __init__(self):
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
        
    @async_retry_with_backoff(max_retries=5, max_backoff=60, backoff_factor=0.5, product_call=False)
    async def tileprices_v2(self, method="GET", params=None, data=None,url=None,headers=None):
        url=self.options["API_CONFIG"]["ENDPOINTS"]["v2_url"]+"tileprices/"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=params, data=data, headers=self.options["API_CONFIG"]["HEADERS"])
        response.raise_for_status()
        return response.json()

    @async_retry_with_backoff(max_retries=5, max_backoff=60, backoff_factor=0.5, product_call=False)
    async def territory_prices(self, method="GET", params=None, data=None,url=None,headers=None):
        all_teritories_payload=[]

        url=self.options["API_CONFIG"]["ENDPOINTS"]["r_url"]+"territory_releases?released=true&sort_by=votes_value&sort_dir=desc&page=1&perPage=12"
        headers_with_auth=self.options["API_CONFIG"]["HEADERS"]

        #inject auth to headers
        headers_with_auth["cookie"]=self.options["API_CONFIG"]["AUTH"]["COOKIE"]
        headers_with_auth["X-CSRFToken"]=self.options["API_CONFIG"]["AUTH"]["X-CSRFTOKEN"]
        
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=params, data=data, headers=headers_with_auth)
        response.raise_for_status()

        all_teritories_payload.extend( response.json()["data"] )
        
        total_pages=response.json()["meta"]["pages"]

        # we know that pages are more than one
        for page in range(2,total_pages+1):
            url=self.options["API_CONFIG"]["ENDPOINTS"]["r_url"]+"territory_releases?released=true&sort_by=votes_value&sort_dir=desc&page=1&perPage="+str(page)
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, params=params, data=data, headers=headers_with_auth)

            response.raise_for_status()
            all_teritories_payload.extend( response.json()["data"] )

        landfield_tier="3"
        for index,territory in enumerate(all_teritories_payload):
            center = territory["attributes"]["center"]
            tile_id = str(lng_lat_to_quadkey_compress(center,zoom=21))

            url=self.options["API_CONFIG"]["ENDPOINTS"]["graphql_url"]

            # The query data with dynamic values
            payload = {
                "query": f"""{{
                getTileIdPrice(tileId: {tile_id}, landfieldTier: {landfield_tier})
                {{
                    essFinal,
                    essDiscountRate,
                    eusdDiscountRate,
                    stakeReq,
                    final,
                    value
                }}
                }}
                """
            }

            async with httpx.AsyncClient() as client:
                method="POST"
                response = await client.request(method, url, params=params, json=payload, headers=headers_with_auth)

            response.raise_for_status()

           
            info_to_update = all_teritories_payload[index]
            sys_price=response.json()["data"]["getTileIdPrice"]["value"]
            info_to_update["estimatedValue"] = sys_price
            info_to_update["estimatedTilesSold"] = int(150000 * np.log(sys_price * 10))

            all_teritories_payload[index]=info_to_update
            
            # ADDED DELAY
            # to play nice on api as we will need to do 100+ calls to get all territory prices
            # ... one day E2 will fix their API =_= ...
            delay = random.uniform(0.25, 0.75)
            ttag = territory["id"] + " | " + territory["attributes"]["territoryCode"] + " | " + territory["attributes"]["territoryName"] + " | " +  territory["attributes"]["countryName"] + " | " + territory["attributes"]["country"]   
            print( "TTAG:    ", str(ttag) )
            print( "estimatedValue: ", str(info_to_update["estimatedValue"]) )
            print( "estimatedTilesSold: ", str(info_to_update["estimatedTilesSold"]) )
            print("Index: ", str(index))
            print("Waiting: ", str(delay))
            print("....")
            await asyncio.sleep(delay)

            
        return all_teritories_payload
        