from pygeocoder import Geocoder
import sqlite3

results = Geocoder.reverse_geocode(19.17496166666666666666666667, 72.86765)
sqlite_file = '/home/pi/Zipcodes.db'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
text = ('SELECT phone from zip WHERE postalcode = "%s"' %results.postal_code)
c.execute(text)
temp = c.fetchone()[0]

conn.close()