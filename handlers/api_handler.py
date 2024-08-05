import json
import httpx
from statics import DirectoryConfig
import functools
import random
import asyncio

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
        
    @async_retry_with_backoff(max_retries=5, max_backoff=60, backoff_factor=0.5, product_call=False)
    async def tileprices_v2(self, method="GET", params=None, data=None,url=None,headers=None):
        url=self.options["API_CONFIG"]["ENDPOINTS"]["v2_url"]+"tileprices/"
        headers=self.headers
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()
        return response.json()