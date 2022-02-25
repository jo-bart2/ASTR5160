import numpy as np
import matplotlib.pyplot as plt
import pymangle
from astropy.coordinates import SkyCoord
import os

# JAB Set up directory pathway
user = os.getenv("USER")
formatter = "/d/www/jordan/public_html/week6"
webdir = formatter.format(user)

# JAB Problem 1
# JAB Use function from previous lecture
def circle_cap(ra, dec, theta):
    """
    Parameters
    ----------
    ra: :class: 'integer'
        The RA in degrees
    dec: :class: 'integer'
         The Dec in degrees
    theta: :class: 'integer'
           The radius of the cap in degrees

    Returns
    -------
    cap: :class: '~numpy.ndarray'
         The array containing the xyz and radius values for the cap
    """

    c = SkyCoord(ra, dec, frame='icrs', unit='deg')
    c.representation_type = 'cartesian'

    cap = np.array([c.x.value, c.y.value, c.z.value, 1-np.cos(np.deg2rad(theta))])

    return cap

# JAB Make two caps: theta=5 (76, 36) and theta=5 (75, 35)
cap1 = circle_cap(76, 36, 5)
cap2 = circle_cap(75, 35, 5)

# JAB Problem 2
# JAB Create function that writes .ply files from caps
def write_ply(name, cap, cp, wt, px, st):
    """
    Parameters
    ----------
    name : :class: 'string'
           The name of the file (without the .ply)
    cap : :class: '~numpy.ndarray'
          Array of arrays containing the xyz values and radius of each cap
    cp : :class: '~numpy.ndarray'
         Array of strings containing number of caps in each polygon
    wt : :class: '~numpy.ndarray'
         Array of strings of the weight of the polygons
    px : :class: '~numpy.ndarray'
         Array of string of the pixel number for the polygons
    st : :class: '~numpy.ndarray'
         Array of strings of the area of the polygons in steradians
    """

    # JAB Open file and write in lines
    file = open(name+'.ply', 'w')

    poly_num = len(cp) # JAB number of polygons
    line1 = '{} polygons\n'.format(poly_num)
    file.write(line1)

    # JAB loop through the number of polygons and the corresponding caps
    for i in range(poly_num):
        file.write('polygon {} ( {} caps, {} weight, {} pixel, {} str):\n'.format(i+1, cp[i], wt[i], px[i], st[i]))
        for j in cap[i]:
            file.write('  {} {} {} {}\n'.format(j[0], j[1], j[2], j[3]))
        
    file.close()

# JAB Write the files with the two caps
write_ply('intersection', [[cap1, cap2]], ['2'], ['1'], ['0'], ['0'])
write_ply('bothcaps', [[cap1], [cap2]], ['1','1'], ['1','1'], ['0','0'], ['0','0'])

# JAB Problem 3
# JAB Read in each of the masks
minter = pymangle.Mangle("intersection.ply")
mboth = pymangle.Mangle("bothcaps.ply")

# JAB Fill each mask with 10000 random points
ra_inter, dec_inter = minter.genrand(10000)
ra_both, dec_both = mboth.genrand(10000)

# JAB Plot points of each mask
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(ra_inter, dec_inter, color='purple', label='Intersection', s=0.7)
ax1.scatter(ra_both, dec_both, color='red', label='Both Mask', s=0.7)
ax1.legend()
ax1.set_xlabel('RA (degrees)')
ax1.set_ylabel('Dec (degrees)')
fig1.savefig(os.path.join(webdir, 'inter_both.png'))
plt.show()
# JAB You can see one mask which includes both full caps and one that is only the intersection of the two

# JAB Problem 4
# JAB Flip the sign of constraint on cap1 and read in
cap1_flip = circle_cap(76, 36, 5)
cap1_flip[3] = cap1_flip[3]*-1
write_ply('intersection_flip', [[cap1_flip, cap2]], ['2'], ['1'], ['0'], ['0'])
mflip1 = pymangle.Mangle('intersection_flip.ply')

# JAB Plot minter and mflip1
ra_flip, dec_flip = mflip1.genrand(10000)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter(ra_inter, dec_inter, color='purple', label='Intersection', s=0.7)
ax2.scatter(ra_flip, dec_flip, color='green', label='Cap 1 Flipped', s=0.7)
ax2.legend()
ax2.set_xlabel('RA (degrees)')
ax2.set_ylabel('Dec (degrees)')
fig2.savefig(os.path.join(webdir, 'inter_flip1.png'))
plt.show()

# JAB Problem 5
# JAB Flip sign of constraint on cap2 and read in
cap2_flip = circle_cap(75, 35, 5)
cap2_flip[3] = cap2_flip[3]*-1
write_ply('intersection_flip2', [[cap1, cap2_flip]], ['2'], ['1'], ['0'], ['0'])
mflip2 = pymangle.Mangle('intersection_flip2.ply')

# JAB Plot minter, mflip1, and mflip2
ra_flip2, dec_flip2 = mflip2.genrand(10000)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.scatter(ra_inter, dec_inter, color='purple', label='Intersection', s=0.7)
ax3.scatter(ra_flip, dec_flip, color='green', label='Cap 1 Flipped', s=0.7)
ax3.scatter(ra_flip2, dec_flip2, color='blue', label='Cap 2 Flipped', s=0.7)
ax3.legend()
ax3.set_xlabel('RA (degrees)')
ax3.set_ylabel('Dec (degrees)')
fig3.savefig(os.path.join(webdir, 'inter_flip2.png'))
plt.show()
