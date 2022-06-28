import numpy as np
import pylab as plt
from astropy.time import Time
from astropy.coordinates import SkyCoord
from matplotlib.patches import Rectangle




def convert(lat, lon):
    """convert lat/lon from the ecliptic to the invariable plane.
    from OSSOS package, written by JJ, I think."""
    secrad = np.pi / 180.0 / 3600.0
    print('this goes in',lat,lon)

    x = np.cos(lon) * np.cos(lat)
    y = np.sin(lon) * np.cos(lat)
    z = np.sin(lat)

    # Invariable plane: values in arcseconds.
    epsilon = 5713.86
    omega = 387390.8

    coseps = np.cos(epsilon * secrad)
    sineps = np.sin(epsilon * secrad)
    cosom = np.cos(omega * secrad)
    sinom = np.sin(omega * secrad)

    xi = x * cosom + y * sinom
    yi = coseps * (-sinom * x + cosom * y) + sineps * z
    zi = - sineps * (-sinom * x + cosom * y) + coseps * z

    lat = np.degrees(np.arcsin(zi))
    lon = np.degrees(np.arctan2(yi, xi))
    print('this goes out',lat,lon)
    return (lat, lon)

#calculate dec along invariable plane for each of these RAs
#make arrays for ecliptic and invariable lats and longs, convert to RA decs to add to plot later
ecl_plane_long=np.arange(0,360,0.1)
ecl_plane_lat=np.zeros(len(ecl_plane_long))
inv_plane_lat,inv_plane_long=convert(np.radians(ecl_plane_lat),np.radians(ecl_plane_long))
ecl_latlon=SkyCoord(ecl_plane_long,ecl_plane_lat,unit='deg',frame='barycentricmeanecliptic')
inv_latlon=SkyCoord(inv_plane_long,inv_plane_lat,unit='deg',frame='barycentricmeanecliptic')
print(ecl_latlon)
ecl_radec=ecl_latlon.transform_to('icrs')
inv_radec=inv_latlon.transform_to('icrs')
ecl_ra=ecl_radec.ra.degree
ecl_dec=ecl_radec.dec.degree
inv_ra=inv_radec.ra.degree
inv_dec=inv_radec.dec.degree

#names for each pointing
disc_point_name=['AS1','AS2','ND1','ND2','AM1','AM2','JA1','JA2','DJ1','DJ2','MA1','MA2']
#new moon dates for each discovery pointing (from spreadsheet https://docs.google.com/spreadsheets/d/1DngZ2HaizZOMQKHuU24uHfS7oNRJyG69CV4N3hhOHAI/edit?usp=sharing)
disc_point_t=Time(['2022-08-26 11:00:00','2022-09-25 11:00:00','2022-11-23 11:00:00','2022-12-23 11:00:00','2023-4-19 11:00:00','2023-5-19 11:00:00','2023-7-17 11:00:00','2023-8-16 11:00:00','2023-12-12 11:00:00','2024-1-11 11:00:00','2024-3-10 11:00:00','2024-4-8 11:00:00'])
#print(disc_point_t.jd)
#RAs for each discovery pointing (from spreadsheet)
disc_point_ra=[348.5,349.5,76.5,77.5,224.5,225.5,313.5,314.5,101.5,102.5,190,191]
#get decs for each pointing by going through invariable plane array and looking for closest value
#there's probably a better way to do this, but this is what I came up with!
disc_point_dec=np.zeros(len(disc_point_ra))
for i in np.arange(0,len(disc_point_ra)):
    diff=np.abs(inv_ra-disc_point_ra[i])
    arg=diff.argmin()
    disc_point_dec[i]=inv_dec[arg]
    print(i,disc_point_ra[i],disc_point_dec[i])

disc_point_radec=SkyCoord(disc_point_ra,disc_point_dec,unit='deg')

#can use this to get pointing coordinates and date for putting into pointing files
#print(disc_point_radec.to_string('hmsdms'))
for i in np.arange(0,len(disc_point_ra)):
    print("poly 4 "+str(disc_point_radec[i].to_string('hmsdms'))+" "+str(disc_point_t[i].jd)+" 0.90 500 "+disc_point_name[i]+".eff")
    print("-0.5 -0.5")
    print("-0.5 0.5")
    print("0.5 0.5")
    print("0.5 -0.5")

a,e,inc,q,r,manom,node,argperi,mag,Hmag,RA,dec=np.genfromtxt("SimulDetect.dat",usecols=(0,1,2,3,4,5,6,7,8,9,16,17),unpack=True)

plt.figure(figsize=(12,8))
plt.plot(RA*15.,dec,'k.')
#plt.scatter(ecl_radec)
plt.plot(ecl_ra,ecl_dec,'.',c='#A4A4A4')
plt.plot(inv_ra,inv_dec,'.',c='r')

plt.plot(disc_point_ra,disc_point_dec,'sm')

plt.ylabel('dec')
plt.xlabel('RA')
plt.xlim(360,0)

plt.savefig('figs/RAdec_det.png')

for i in np.arange(0,len(disc_point_name)):
    fig, ax = plt.subplots(figsize=(6,6))
    plt.title(disc_point_name[i])
    plt.plot(RA*15.,dec,'k.')
    plt.plot(ecl_ra,ecl_dec,'.',c='#A4A4A4')
    plt.plot(inv_ra,inv_dec,'.',c='r')

    ax.add_patch(Rectangle((disc_point_ra[i]-0.5, disc_point_dec[i]-0.5), 1.0, 1.0,facecolor='none',edgecolor='k'))

    plt.ylabel('dec')
    plt.xlabel('RA')
    plt.xlim(disc_point_ra[i]+1.,disc_point_ra[i]-1.)
    plt.ylim(disc_point_dec[i]-1.,disc_point_dec[i]+1.)
    plt.savefig('figs/'+disc_point_name[i]+'.png')

#plt.show()