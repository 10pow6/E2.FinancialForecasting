import math
import numpy as np

def lng_lat_to_quadkey_compress(lng_lat, zoom):
    lng, lat = lng_lat
    
    def to_rad(x):
        return x * math.pi / 180
    
    tilex = math.floor((lng + 180) / 360 * (1 << zoom))
    tiley = math.floor((1 - math.log(math.tan(to_rad(lat)) + 1 / math.cos(to_rad(lat))) / math.pi) / 2 * (1 << zoom))
    
    bitmap = []
    for idx in range(zoom):
        mask = 1 << (zoom - 1 - idx)
        digit = 0
        if (tilex & mask) != 0:
            digit = 1
        if (tiley & mask) != 0:
            digit += 2
        bitmap.extend([int((digit >> (1 - i)) & 1) for i in range(2)])
    
    result = sum(val * (2 ** idx) for idx, val in enumerate(bitmap))
    return result * 100 + zoom

'''
# Example usage:
    result = lng_lat_to_quadkey_compress([166.96405, -0.531397], 21)
    print(result)  # Output: 162837496849121
'''

# if calling w/ textual work
# async def spend_worker(tiles_sold=0,sys_val=0,tier=0,country_code=""):   
def spend_worker(tiles_sold=0,sys_val=0,tier=0,country_code=""):   
    base = 0.1
    # exponent_base = np.e       ### standard e
    # exponent_base = 2.7142     ### e2 economist rate
    # exponent_base = 2.7141     ### butt og rate
    
    if( country_code == "__" ): #exception for lower international price
        base = 0.01
        
    if tier == 1: # Landfield tier 1 formula
        gen = (    base * ( np.e ** (x/100000) ) for x in range(0,tiles_sold)    )
    elif tier == 2: # Landfield tier 2 formula
        gen = (    base * ( np.e ** (x/150000) ) for x in range(0,tiles_sold)    )
    elif tier == 3: # Landfield tier 3 formula
        gen = (    base * ( np.e ** (x/150000) ) for x in range(0,tiles_sold)    )   

    return {
        "countryCode": country_code,
        "tier":tier,
        "userSpend": float(np.sum(np.fromiter(gen,np.float64))),
        "mCap": tiles_sold*sys_val
    }