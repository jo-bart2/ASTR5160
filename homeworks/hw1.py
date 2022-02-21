import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy.table import Table, QTable
import astropy.units as u
import argparse

def do_it_all(m):
    """Should have a better docstring than this."""

    # JAB Read in the data from the file and separate into ra and dec
    data = Table.read('/d/scratch/ASTR5160/week4/HW1quasarfile.txt', format='ascii.no_header')

    # ADM Read in the data from the file and separate into ra and dec.
    ra = ["{}h{}m{}s".format(q[0:2], q[2:4], q[4:9]) for q in data["col1"]]
    dec = ["{}d{}m{}s".format(q[9:12], q[12:14], q[14:18]) for q in data["col1"]]
    c = SkyCoord(ra, dec, frame='icrs')

    # JAB Determine time and location
    kitt = EarthLocation.of_site('kpno')
    utcoffset = -7*u.hour

    if m in ['1', '3', '5', '7', '8', '10', '12']:
        days = range(1,32)
    elif m in ['4', '6', '9', '11']:
        days = range(1,31)
    else:
        days = range(1,29)

    times = ['2022-' + m + '-' + str(d) + ' 23:00:00' for d in days]
    dates = Time(times, format='iso') - utcoffset

    # ADM Find airmass for each of the quasars and create lists of each eventual column
    airmasses = [c.transform_to(AltAz(obstime=d, location=kitt)).secz for d in dates]
    indexes = np.array([np.argmin(np.where(am > 0, am, 1e16)) for am in airmasses])
    airmass = np.array([np.min(np.where(am > 0, am, 1e16)) for am in airmasses])

    # ADM Create and print out table of values
    table = QTable([dates, data["col1"][indexes], c[indexes].ra.value, c[indexes].dec.value, airmass],
                   names=['Date (UTC)', 'Quasar Coordinates', 'RA (o)', 'Dec (o)', 'Airmass'])

    print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Determine the minimum airmass for quasars for a month of the year")
    parser.add_argument('month', help="A particular month of the year")
    args = parser.parse_args()
    m = args.month
    do_it_all(m)

