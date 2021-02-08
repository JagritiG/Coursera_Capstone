from geopy.geocoders import Nominatim

# get the latitude and longitude values of San Diego
address = 'Bay Ho,San Diego,CA'

# define an instance of the geocoder
geolocator = Nominatim(user_agent='sd')
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude

print("The geographical coordinates are: {}, {}.".format(latitude, longitude))



