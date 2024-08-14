import math

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