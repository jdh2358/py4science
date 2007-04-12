"""
parse and load ge.csv into a record array
"""
import time, datetime, csv
import dateutil.parser
import numpy

fh = file('data/ge.csv')
reader = csv.reader(fh)
header = reader.next()

rows = []
for date, open, high, low, close, volume, adjclose in reader:
    date = dateutil.parser.parse(date).date()
    volume = int(volume)
    open, high, low, close, adjclose = map(float, (
        open, high, low, close, adjclose))
    rows.append((date, open, high, low, close, volume, adjclose))

#rows = load('data/ge.csv', skiprows=1, converters={0:datestr2num}, delimiter=',')

r = numpy.rec.fromrecords(rows, names='date,open,high,low,close,volume,adjclose')
fh.close()
