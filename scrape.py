#!/usr/bin/env python3

from lxml import html
import requests
import utm

url = "http://webhotel2.gisline.no/gislinewebplan_1149/gl_planarkiv.aspx?planid=670"

page = requests.get(url)
tree = html.fromstring(page.content)
table = tree.xpath('//*[@id="ctl00_divDispentions"]')[0][1]

latlons = []
lats = []
lons = []
dates = []

#toFind = "Forbud mot tiltak mv. langs sjÃ¸ og vassdrag"
to_find = "vassdrag"

rows = table.xpath('./tr')
for row in rows[1:]: # loop through rows, skip header
    cols = row.xpath('./td')

    if to_find in cols[4].xpath("string()"): # check value of column "Dispensasjonstype" in this row
        last_div = cols[-1].xpath('./div')[0]
        coord = last_div.xpath("string()")

        i = coord.find("X:")
        j = coord[i:].find("\r")
        x = coord[i+3:i+j]
        x = float(x.replace(',', '.'))

        i = coord.find("Y:")
        j = coord[i:].find("\r")
        y = coord[i+3:i+j]
        y = float(y.replace(',', '.'))

        easting = y
        northing = x
        latlon = utm.to_latlon(easting, northing, 32, northern = True)
        latlons.append([latlon[0], latlon[1]])
        lats.append(latlon[0])
        lons.append(latlon[1])

        datestr = cols[0].xpath('string()')
        sekvensnr = cols[1].xpath('string()')
        dates.append(datestr + ", " + sekvensnr)

import gmplot

gmap = gmplot.GoogleMapPlotter.from_geocode("Kopervik", zoom = 11)
gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/" # fix

for (lat, lon), date in zip(latlons, dates):
    gmap.marker(lat, lon, text = date)
    
gmap.draw("mymap.html")
