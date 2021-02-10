# Extract list of neighborhoods of the San Diego city from webpage and create dataset
# url: https://en.wikipedia.org/wiki/Template:Toronto_neighbourhoods
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

for ods in soup.findAll(class_="navbox-list navbox-odd hlist"):
    for a in ods.find_all('a'):
        odd.append([a["href"], a["title"], a.text])
# print(odd)

for eve in soup.findAll(class_="navbox-list navbox-even hlist"):
    for a in eve.find_all('a'):
        even.append([a["href"], a["title"], a.text])
# print(even)

# concatenate these two list
neighbors = odd + even
# print(neighbors)


# create dataframe
toronto_df = pd.DataFrame()

toronto_df['toronto_Neighborhoods'] = neighbors
# print(sd_df.head(10))

# pre-process data
neighborhoods = []
address = []

for i in toronto_df['toronto_Neighborhoods']:
    neighborhoods.append(i[-1])

toronto_df['Neighborhoods'] = neighborhoods
# print(sd_df.head(10))

# create a new df
toronto_neighbors = toronto_df[['Neighborhoods']]
# print(sd_neighbors.head(10))
# print(sd_neighbors.shape)

# Add full address
for val in toronto_neighbors['Neighborhoods']:
    ads = val + ',' + 'Toronto' + ',' + 'Ontario'
    address.append(ads)

toronto_neighbors['Address'] = address
# print(sd_neighbors.head())


# save to csv
toronto_neighbors.to_csv("../data/toronto_neighbors.csv", index=False)

# get geographical coordinates of each neighborhood
geolocator = Nominatim(user_agent="toronto_hoods")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
toronto_neighbors['Location'] = toronto_neighbors['Address'].apply(geocode)

toronto_neighbors['Coordinates'] = toronto_neighbors['Location'].apply(lambda loc: tuple(loc.point) if loc else None)

# add columns tat and lng
lat = []
lng = []

for i in toronto_neighbors['Coordinates']:
    if i is not None:
        lat.append(i[0])
        lng.append(i[1])
    else:
        lat.append(np.nan)
        lng.append(np.nan)

toronto_neighbors['Latitude'] = lat
toronto_neighbors['Longitude'] = lng

print(toronto_neighbors.head(5))


# Save zip file
compression_opts = dict(method='zip',
                        archive_name='toronto_neighborhoods.csv')
toronto_neighbors.to_csv('../data/toronto_neighborhoods.zip', index=False,
          compression=compression_opts)

