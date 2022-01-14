from django.contrib.gis.geoip2 import GeoIP2

# Our Helper Function

# to get live ip addres when your website is hosted
def get_ip(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else: 
        ip = request.META.get('REMOTE_ADDR')
    return ip

# getting the values of destination by geopy    
def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return  country, city, lat, lon

# to get the center between location and destination and if destination is not given 
def get_center(latA, lonA, latB=None, lonB=None):
    cord= (latA, lonA)
    if latB:
        cord = [(latA+latB)/2,(lonA+lonB)/2]
    return cord

# function to adjuxt the jooming of frame by distance between them
def get_zoom(distance):
    if distance <= 100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2
