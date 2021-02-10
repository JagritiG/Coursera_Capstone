# Extract list of neighborhoods of the San Diego city from webpage and create dataset
# url: https://en.wikipedia.org/wiki/Template:Neighborhoods_of_San_Diego
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# load the webpage
url = "https://en.wikipedia.org/wiki/Template:Toronto_neighbourhoods"
r = requests.get(url)

# convert to a beautiful soup object
soup = bs(r.content, 'lxml')

# print out the HTML
contents = soup.prettify()
# print(contents)

# Extract table data
nav_box = soup.find(class_="navbox")
# print(nav_box.prettify())

odd = []
even = []

for ods in soup.findAll(class_="navbox-list navbox-odd"):
    for a in ods.find_all('a'):
        odd.append([a["href"], a["title"], a.text])
# print(odd)

for eve in soup.findAll(class_="navbox-list navbox-even"):
    for a in eve.find_all('a'):
        even.append([a["href"], a["title"], a.text])
# print(even)

# concatenate these two list
neighbors = odd + even
# print(neighbors)


# create dataframe
sd_df = pd.DataFrame()

sd_df['SD_Neighborhoods'] = neighbors
# print(sd_df.head(10))

# pre-process data
neighborhoods = []
address = []

for i in sd_df['SD_Neighborhoods']:
    neighborhoods.append(i[-1])

sd_df['Neighborhoods'] = neighborhoods
# print(sd_df.head(10))

# create a new df
sd_neighbors = sd_df[['Neighborhoods']]
# print(sd_neighbors.head(10))
# print(sd_neighbors.shape)

# Add full address
for val in sd_neighbors['Neighborhoods']:
    ads = val + ',' + 'San Diego' + ',' + 'CA'
    address.append(ads)

sd_neighbors['Address'] = address
# print(sd_neighbors.head())


# save to csv
sd_neighbors.to_csv("../data/sd_neighbors.csv", index=False)

# get geographical coordinates of each neighborhood
geolocator = Nominatim(user_agent="sd_hoods")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
sd_neighbors['Location'] = sd_neighbors['Address'].apply(geocode)

sd_neighbors['Coordinates'] = sd_neighbors['Location'].apply(lambda loc: tuple(loc.point) if loc else None)

# add columns tat and lng
lat = []
lng = []

for i in sd_neighbors['Coordinates']:
    if i is not None:
        lat.append(i[0])
        lng.append(i[1])
    else:
        lat.append(np.nan)
        lng.append(np.nan)

sd_neighbors['Latitude'] = lat
sd_neighbors['Longitude'] = lng

print(sd_neighbors.head(5))


# Save zip file
compression_opts = dict(method='zip',
                        archive_name='sd_neighborhoods.csv')
sd_neighbors.to_csv('../data/sd_neighborhoods.zip', index=False,
          compression=compression_opts)

