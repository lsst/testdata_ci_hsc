This is a pared-down version of the ps1_pv3_3pi_20170110 reference catalog,
for the purpose of the LSST ci_hsc package, containing the following shards:

    189584 189648



Construction of the ps1_pv3_3pi_20170110 reference catalog
==========================================================

This reference catalog, intended for use with the LSST Science Pipelines
(https://pipelines.lsst.io) was constructed from the "3pi.pv3.20160422" DVO
catalog of Processing Version 3 of the Pan-STARRS1 3pi survey, released to
the Pan-STARRS1 Science Consortium. Following the public release of this data
in December 2016 (http://panstarrs.stsci.edu), you may distribute this catalog
freely.

This format of the catalog contains 2,990,470,528 point sources at
Dec > -30 deg to i ~ 22.5 mag, and has a total size of 423 GB. 

Questions and comments about this format of the PS1 catalog may be directed
to Paul Price (price@astro.princeton.edu) or submitted to
https://community.lsst.org .

Users of this catalog should include the following acknowledgement in
publications:

    The Pan-STARRS1 Surveys (PS1) have been made possible through contributions
    of the Institute for Astronomy, the University of Hawaii, the Pan-STARRS
    Project Office, the Max-Planck Society and its participating institutes,
    the Max Planck Institute for Astronomy, Heidelberg and the Max Planck
    Institute for Extraterrestrial Physics, Garching, The Johns Hopkins
    University, Durham University, the University of Edinburgh, Queen's
    University Belfast, the Harvard-Smithsonian Center for Astrophysics,
    the Las Cumbres Observatory Global Telescope Network Incorporated, the
    National Central University of Taiwan, the Space Telescope Science
    Institute, the National Aeronautics and Space Administration under Grant
    No. NNX08AR22G issued through the Planetary Science Division of the NASA
    Science Mission Directorate, the National Science Foundation under Grant
    No. AST-1238877, the University of Maryland, and Eotvos Lorand University
    (ELTE), the Los Alamos National Laboratory, and the Gordon and Betty Moore
    Foundation.

Relevant papers for information and citation include:

* Chambers et al., "The Pan-STARRS1 Surveys", 2016arXiv161205560C
* Magnier et al., "The Pan-STARRS Data Processing System", 2016arXiv161205240M
* Waters et al., "Pan-STARRS Pixel Processing: Detrending, Warping, Stacking",
    2016arXiv161205245W
* Magnier et al., "Pan-STARRS Pixel Analysis: Source Detection and
    Characterization", 2016arXiv161205244M
* Magnier et al., "Pan-STARRS Photometric and Astrometric Calibration",
    2016arXiv161205242M
* Flewelling et al., "The Pan-STARRS1 Database and Data Products",
    2016arXiv161205243F
* Tonry et al., "The Pan-STARRS1 Photometric System", 2012ApJ...750...99T
* Schlafly et al., "Photometric Calibration of the First 1.5 Years of the
    Pan-STARRS1 Survey", 2012ApJ...756..158S


The DVO catalog
---------------

The 3pi.pv3.20160422 DVO catalog was released to PS1SC members before the
public data release in December 2016, so download presently requires a
username, passwrod and that the requesting IP address is recognised as that
of a member.

The format of the catalog is described in 2016arXiv161205240M.  Briefly, DVO
uses multiple files for each area.  For our purposes, we care only about the
"*.cpt" and "*.cps" files: the "*.cpt" files contain a single-row summary
(position and index) for each object, and the "*.cps" files contains one row
(fluxes, etc.) for each photcode for each object.  Other files include
measurements for each detection of an object, and weak lensing shape
measurements, but we're not going to download those.

The position of a measurement in the cps file is N*i+C-1, where:
* N is the number of secondary photcodes: from the Photcodes.dat table, where
    TYPE=2 (there are 9: grizyJHKw).
* i is the index of the source in the cpt file.
* C is the CODE for the filter from the Photcodes.dat table (grizy are 1..5).
* -1 is because the codes are unit-indexed.

The mapping of database columns to DVO columns is:

    objID           cpt:EXT_ID
    ra              cpt:RA
    dec             cpt:DEC
    xMeanPSFMag     cps:MAG
    xMeanPSFMagErr  cps:MAG_ERR
    xStackPSFMag    cps:MAG_PSF_STK
    xStackPSFMagErr cps:FLUX_PSF_STK_ERR --> magnitude error
    xFlags          cps:(0x7fff & FLAGS) | ((FLAGS >> 11) & 0x2000)
    objInfoFlag     cpt:FLAGS
    qualityFlag     cpt:FLAGS >> 24 & 0xFF

Download the DVO catalog
------------------------

wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n0000/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n0730/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n1500/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n2230/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n3000/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n3730/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n4500/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n5230/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n6000/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n6730/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n7500/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/n8230/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s0000/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s0730/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s1500/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s2230/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s3000/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s3730/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s4500/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s5230/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s6000/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s6730/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s7500/ &
wget -c -r -np -nH --user=XXX --password=XXX -A "*.cpt" -A "*.cps" http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/s8230/ &

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.cpt" | wc -l
151984
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ du -s
4.0T    .


Top-level files in the catalog and their sizes:

   AstroMap.fits  6930665280
   flatcorr.fits  167040
   flatfield.fits 99362880
   HostTable.dat  8444
   Images.dat     15476924160
   Photcodes.dat  118080
   SkyTable.fits  9077760

I believe that these are not required to extract data from the cpt and cps
files, but are used by DVO in performing the calibration (the results of
which are written into the cpt and cps files).

wget -c -np -nH --user=XXX --password=XXX http://dvodist.ipp.ifa.hawaii.edu/3pi.pv3.20160422/Photcodes.dat

Confirmed that there are 9 photocodes.


Check the DVO catalog contents
------------------------------

Spot-checking that the values in the DVO tables don't need any modification.
(Gene Magnier says they don't; but checking just in case.)

In 3246.00.cpt, line 33333 (unit-indexed):
>>> ra, dec = 0.39280180542574594, 45.286118215179194
In the cps file, corresponding values should start at 9*(33333-1)+1=299989
PSF mags:
g   21.985485 0.035457805
r   20.877203 0.06612972
i   20.302347 0.023914162
z   19.819653 0.03863905
y   19.499033 0.041598786

From the database at STScI, get:

objName objID   raMean  decMean raMeanErr   decMeanErr  nDetections htmID   zoneID  randomID    projectionID    skyCellID   processingVersion   objInfoFlag qualityFlag raStack decStack    raStackErr  decStackErr epochMean   posMeanChisq    lambda  beta    l   b   nStackObjectRows    nStackDetections    ng  nr  ni  nz  ny  gQfPerfect  gMeanPSFMag gMeanPSFMagErr  gMeanPSFMagStd  gMeanPSFMagNpt  gMeanPSFMagMin  gMeanPSFMagMax  gMeanKronMag    gMeanKronMagErr gMeanKronMagStd gMeanKronMagNpt gMeanApMag  gMeanApMagErr   gMeanApMagStd   gMeanApMagNpt   gFlags  rQfPerfect  rMeanPSFMag rMeanPSFMagErr  rMeanPSFMagStd  rMeanPSFMagNpt  rMeanPSFMagMin  rMeanPSFMagMax  rMeanKronMag    rMeanKronMagErr rMeanKronMagStd rMeanKronMagNpt rMeanApMag  rMeanApMagErr   rMeanApMagStd   rMeanApMagNpt   rFlags  iQfPerfect  iMeanPSFMag iMeanPSFMagErr  iMeanPSFMagStd  iMeanPSFMagNpt  iMeanPSFMagMin  iMeanPSFMagMax  iMeanKronMag    iMeanKronMagErr iMeanKronMagStd iMeanKronMagNpt iMeanApMag  iMeanApMagErr   iMeanApMagStd   iMeanApMagNpt   iFlags  zQfPerfect  zMeanPSFMag zMeanPSFMagErr  zMeanPSFMagStd  zMeanPSFMagNpt  zMeanPSFMagMin  zMeanPSFMagMax  zMeanKronMag    zMeanKronMagErr zMeanKronMagStd zMeanKronMagNpt zMeanApMag  zMeanApMagErr   zMeanApMagStd   zMeanApMagNpt   zFlags  yQfPerfect  yMeanPSFMag yMeanPSFMagErr  yMeanPSFMagStd  yMeanPSFMagNpt  yMeanPSFMagMin  yMeanPSFMagMax  yMeanKronMag    yMeanKronMagErr yMeanKronMagStd yMeanKronMagNpt yMeanApMag  yMeanApMagErr   yMeanApMagStd   yMeanApMagNpt   yFlags  Ang Sep (')
PSO J000134.268+451710.163  162340003927854012  00 01 34.272    +45 17 10.03    0.015   0.016   53  16836277578733  16234   0.825292547070694   2225    34  3   444915712   53  00 01 34.269    +45 17 10.16    0.001   0.001   55936.29421296  1.457   22.19887281378932   40.54697590262472   113.808085852593    -16.70034366172768  -999    5   4   12  13  12  12  0.999   21.985  0.026   0.055   3   21.927  22.035  21.543  0.132   0.492   4   21.459  0.240   0.527   4   16892216    0.999   20.877  0.067   0.238   11  20.602  21.424  20.644  0.059   0.200   11  20.608  0.084   0.197   11  16892216    0.999   20.302  0.022   0.196   11  19.954  20.652  19.861  0.027   0.131   8   19.825  0.028   0.112   8   16892216    0.999   19.820  0.042   0.131   10  19.605  19.969  19.496  0.021   0.157   9   19.470  0.029   0.136   10  16892216    1.000   19.499  0.037   0.149   10  19.304  19.851  19.122  0.054   0.168   10  19.058  0.049   0.170   10  16892216    3.467e-7

The magnitudes appear to be identical (within rounding)!  The quoted errors are
slightly different --- no big deal.


Recompress everything with gzip
-------------------------------

A warning about the DVO files, from http://dvodist.ipp.ifa.hawaii.edu :

       Note that all but the first 4 DVOs are distributed with compressed
       FITS tables following the convention specified by Pense et al
       (http://arxiv.org/pdf/1201.1340v1.pdf). This convention has not yet
       been ratified by the FITS standard, though is expected by Summer
       2016. As a result, standard FITS tools will have trouble reading 
       these tables. Two options which exist: 1) download the current IPP
       / Ohana tools and use these either to read the tables (with e.g.,
       dvo or mana), or to uncompress the tables (with the program  
       ftable). 2) download the latest version of fpack and use funpack to
       uncompress the tables. In the later case, there is a small
       inconsistency between our implementation and funpack: if funpack  
       finds the header keyword ZTILELEN and the expected output table   
       length ZNAXIS2 is < ZTILELEN, funpack will fail. (We treat ZTILELEN
       as a maximum block size, and so handle this case as we handle the
       last block in a table. The white paper is not explicit in how to
       handle this case). It is possible to use funpack to uncompress  
       these tables by modifying the value of ZTILELEN to match ZNAXIS2.

That's rather annoying: the tool most everyone has available doesn't work
out-of-the-box, and the tool that does work is a bit obscure. In order to
make this more convenient, decompress everything and recompress it with
gzip.  That way, cfitsio and pyfits will just work without having to do
anything special. And I think it saves a bit of space as well (maybe 25%?).

I'll use the Ohana tool 'ftable' to do the decompression because that's what
was used to compress it in the first place. cfitsio's 'funpack' tool would work
too if you set ZTILELEN = ZNAXIS2 if and only if ZTILELEN > ZNAXIS2.

cd ~/Software
svn co http://svn.pan-starrs.ifa.hawaii.edu/repo/ipp/trunk/Ohana
cd Ohana
configure
make

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.cp?" | xargs -n 1 -P 20 -I {} bash -c '~/Software/Ohana/src/tools/bin/ftable.lin64 -uncompress {} {}.fits ; gzip {}.fits'

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.fits.gz" | wc -l
303968

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ rm */*.cp[ts]


Extract sources of interest
---------------------------

Convert the CPT+CPS files to a single FITS file, and extract sources we want
in our catalog.

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ unset EUPS_DIR EUPS_SHELL EUPS_PATH EUPS_PKGROOT SETUP_EUPS
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ . /tigress/HSC/LSST/stack_20160915/eups/bin/setups.sh 
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ setup miniconda2
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ setup -t w_2017_2 lsst_distrib
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ path_prepend PYTHONPATH /tigress/HSC/users/price/ps1_pv3/python/
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ path_prepend PATH /tigress/HSC/users/price/ps1_pv3/bin/
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ setup -j -r ~/LSST/ctrl_pool  # tickets/DM-5989 branch
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ export OMP_NUM_THREADS=1

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.cpt.fits.gz" | xargs -n 32 -P 20 readDvo.py

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.extract.fits.gz" | wc -l
151548

Some of the inputs didn't produce an output because there were no good sources,
and some just failed for some unknown reason.

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.cpt" | sed 's|\.cpt$||' | sort > cptFiles.txt &
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.extract.fits.gz" | sed 's|\.extract\.fits\.gz$||' | sort > extractFiles.txt
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ comm -23 cptFiles.txt extractFiles.txt | wc -l
436
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ comm -23 cptFiles.txt extractFiles.txt | xargs -n 32 -P 20 -I{} readDvo.py {}.cpt.fits.gz 

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.extract.fits.gz" | sed 's|\.extract\.fits\.gz$||' | sort > extractFiles2.txt
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ comm -23 cptFiles.txt extractFiles2.txt | wc -l
81
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ comm -23 cptFiles.txt extractFiles2.txt | xargs -I{} readDvo.py {}.cpt.fits.gz 

Now the failures are all files with no good sources.

Concatenate the *.extract.fits.gz files so we're not dealing with a bunch of
small files.

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.extract.fits.gz" | sed 's|\...\.extract\.fits.gz$||' | sort | uniq | xargs -n 1 -P 20 -I {} sh -c "concatenate.py {}.all.fits.gz {}.*.extract.fits.gz"

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.extract.fits.gz" | sed 's|\...\.extract\.fits.gz$||' | sort | uniq | wc -l
9494
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ find . -name "*.all.fits.gz" | wc -l
9494


Construct the LSST catalog
--------------------------

mkdir DATA
echo lsst.obs.test.TestMapper > DATA/_mapper

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ ingestIndexReferenceDriver.py DATA '*/*.all.fits.gz' --cores 25
[...]
ingester INFO: Extracted a total of 2990470528 sources
Tue Jan 10 05:10:18 EST 2017
Done.

pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422 $ ls DATA/ref_cats/ps1_pv3_3pi_20170110/ | wc -l
130927
pprice@tigressdata:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422/DATA/ref_cats $ du
423G    ./ps1_pv3_3pi_20170110
423G    .


Test drive
----------

pprice@tiger-sumire:/tigress/HSC/HSC/ref_cats $ ln -s /tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422/DATA/ref_cats/ps1_pv3_3pi_20170110/

pprice@tiger-sumire:/tigress/HSC/users/price/ps1_pv3 $ cat processCcd-overrides.py
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.astromRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
config.calibrate.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

pprice@tiger-sumire:/tigress/HSC/users/price/ps1_pv3 $ processCcd.py /tigress/HSC/HSC --rerun price/test --id visit=1248 ccd=49 -C processCcd-overrides.py 
[...]
processCcd.calibrate.astromRefObjLoader INFO: Loading reference objects using center (1023.5, 2087.5) pix = Fk5Coord(150.1627927, 2.2474638, 2000.00) sky and radius 0.112946975951 deg
processCcd.calibrate.astromRefObjLoader INFO: Loaded 1422 reference objects
processCcd.calibrate.astrometry.matcher INFO: filterStars purged 0 reference stars, leaving 1422 stars
processCcd.calibrate.astrometry.matcher INFO: Purged 2678 unusable sources, leaving 499 usable sources
processCcd.calibrate.astrometry.matcher INFO: Matched 469 sources
processCcd.calibrate.astrometry.matcher INFO: filterStars purged 0 reference stars, leaving 1422 stars
processCcd.calibrate.astrometry.matcher INFO: Purged 2678 unusable sources, leaving 499 usable sources
processCcd.calibrate.astrometry.matcher INFO: Matched 403 sources
processCcd.calibrate.astrometry.matcher INFO: filterStars purged 0 reference stars, leaving 1422 stars
processCcd.calibrate.astrometry.matcher INFO: Purged 2678 unusable sources, leaving 499 usable sources
processCcd.calibrate.astrometry.matcher INFO: Matched 382 sources
processCcd.calibrate.astrometry INFO: Matched and fit WCS in 3 iterations; found 382 matches with scatter = 0.099 +- 0.068 arcsec
processCcd.calibrate.photoRefObjLoader INFO: Loading reference objects using center (1023.5, 2087.5) pix = Fk5Coord(150.1619008, 2.2428156, 2000.00) sky and radius 0.112181296012 deg
processCcd.calibrate.photoRefObjLoader INFO: Loaded 1405 reference objects
processCcd.calibrate.photoCal.matcher INFO: filterStars purged 0 reference stars, leaving 1405 stars
processCcd.calibrate.photoCal.matcher INFO: Purged 2851 unusable sources, leaving 326 usable sources
processCcd.calibrate.photoCal.matcher INFO: Matched 300 sources
processCcd.calibrate.photoCal INFO: Found 300 matches with scatter = 0.079 +- 0.062 arcsec; 
processCcd.calibrate.photoCal WARN: No 'photometric' flag key found in reference schema.
processCcd.calibrate.photoCal INFO: Applying color terms for filterName='i', config.photoCatName=ps1_pv3_3pi_20170110 because config.applyColorTerms is True
processCcd.calibrate.photoCal INFO: Magnitude zero point: 32.999018 +/- 0.000356 from 54 stars
processCcd.calibrate INFO: Photometric zero-point: 32.999018


The log contains a warning:

    processCcd.calibrate.photoCal WARN: No 'photometric' flag key found in reference schema.

This can be ignored --- there's no need for a 'photometric' flag because everything
has been calibrated.


Field selections
----------------

The 423 GB size of this catalog may be prohibitive for individual use.  In that
case, it's possible to copy individual files required for particular regions of
interest. Just grab the <shard>.fits files (plus config.py and this README.txt
file), where the list of shards is calculated from this code:

    from lsst.meas.algorithms.htmIndexer import HtmIndexer
    from lsst.afw.coord import IcrsCoord
    from lsst.afw.geom import degrees

    def getShards(ra, dec, radius):
        htm = HtmIndexer(depth=7)
        shards, onBoundary = htm.get_pixel_ids(IcrsCoord(ra*degrees, dec*degrees), radius*degrees)
        return shards


Some common fields (using the PS1 Medium-Deep pointing centers and a
radius of 2 deg) are:

M31       10.675   +41.267
       258146, 258147, 258152, 258153, 258154, 258155, 258156, 258157,
       258159, 258273, 258275, 258276, 258278, 258279, 258286, 258287,
       256144, 256146, 256147, 258064, 258065, 258067, 258132, 258144,
       258145, 258149, 258150, 258151, 258158, 258160, 258161, 258162,
       258163, 258166, 258174, 258248, 258272, 258274, 258277, 258281,
       258282, 258283, 258284, 258285, 258292, 258294, 258295
SXDS      34.5     -5.000
       133200, 133201, 133202, 133203, 133209, 133213, 133214, 133215,
       133280, 133312, 133314, 133315, 133968, 134048, 134049, 134050,
       134051, 134052, 134053, 134054, 134055, 134058, 134060, 134061,
       134062, 134063, 134070, 134080, 133188, 133205, 133206, 133207,
       133208, 133210, 133211, 133212, 133240, 133281, 133282, 133283,
       133313, 133321, 133325, 133326, 133327, 133969, 133970, 133971,
       134024, 134056, 134057, 134059, 134064, 134065, 134067, 134068,
       134069, 134071, 134076, 134078, 134079, 134081, 134082, 134083,
       134086, 134094
XMM-LSS   35.875   -4.250
       133201, 133202, 133203, 133204, 133205, 133206, 133207, 133208,
       133209, 133210, 133211, 133212, 133213, 133214, 133215, 133241,
       133313, 133314, 133315, 133320, 133321, 133322, 133323, 133324,
       133325, 133326, 133327, 134054, 133188, 133200, 133224, 133232,
       133234, 133235, 133240, 133242, 133243, 133244, 133245, 133247,
       133280, 133282, 133283, 133289, 133293, 133312, 133317, 133318,
       133319, 133348, 133364, 133365, 133367, 133370, 133372, 134024,
       134048, 134049, 134051, 134052, 134053, 134055, 134060, 134062,
       134063, 134068
CDFS      53.100   -27.800
       147042, 147048, 147049, 147051, 147053, 147169, 147172, 147173,
       147174, 147175, 147180, 147182, 147183, 147188, 147028, 147040,
       147041, 147043, 147050, 147052, 147054, 147055, 147056, 147057,
       147059, 147144, 147146, 147147, 147168, 147170, 147171, 147177,
       147178, 147179, 147181, 147185, 147189, 147190, 147191, 147198
Cosmos    150.000  +2.200
       231828, 231829, 231830, 231831, 231834, 231836, 231838, 231839,
       231844, 231845, 231847, 231850, 231852, 231856, 231857, 231858,
       231859, 231860, 231861, 231862, 231863, 231865, 231866, 231867,
       231868, 231869, 231870, 231871, 231812, 231813, 231815, 231816,
       231817, 231818, 231819, 231820, 231825, 231826, 231827, 231832,
       231833, 231835, 231837, 231846, 231848, 231849, 231851, 231853,
       231854, 231855, 231864, 231876, 231890, 231896, 231897, 231899,
       231901, 231928, 232324, 232344, 232345, 232347, 232376
Lockman   161.917  +58.083
       236308, 236310, 236311, 236328, 236336, 236500, 236501, 236503,
       236517, 236518, 236519, 236520, 236521, 236522, 236523, 236524,
       236525, 236526, 236527, 236528, 236529, 236530, 236531, 236534,
       236542, 236305, 236309, 236316, 236318, 236319, 236329, 236330,
       236331, 236337, 236338, 236339, 236386, 236392, 236393, 236395,
       236397, 236502, 236506, 236508, 236510, 236511, 236512, 236513,
       236514, 236515, 236516, 236532, 236533, 236535, 236537, 236540,
       236541, 236543
DEEP2-1   213.704  +53.083
       218400, 218401, 218403, 225808, 225809, 225810, 225811, 225814,
       225821, 225822, 225823, 226016, 226017, 226018, 226019, 226025,
       226029, 218402, 218406, 218413, 218414, 218415, 218512, 218576,
       218577, 218579, 225812, 225813, 225815, 225817, 225818, 225819,
       225820, 225842, 225888, 225890, 225891, 225897, 225901, 226022,
       226024, 226026, 226027, 226028, 226030, 226031
ELAIS-N1  242.787  +54.950
       219732, 219733, 219735, 219748, 219749, 219750, 219751, 219752,
       219753, 219754, 219755, 219756, 219757, 219758, 219759, 219760,
       219761, 219762, 219763, 219764, 219766, 219767, 219773, 219774,
       219775, 219848, 219876, 219892, 219720, 219722, 219723, 219734,
       219738, 219740, 219742, 219743, 219745, 219746, 219747, 219765,
       219769, 219770, 219771, 219772, 219849, 219850, 219851, 219853,
       219873, 219877, 219878, 219879, 219886, 219893, 219894, 219895,
       227716, 227730, 227736, 227737, 227739, 227741, 227768
SA22      334.188  +0.283
       189956, 189970, 189976, 189977, 189978, 189979, 189980, 189981,
       189983, 190008, 198920, 198921, 198923, 198945, 198946, 198947,
       198948, 198949, 198950, 198951, 198954, 198956, 198957, 198958,
       198959, 198964, 198966, 198967, 189953, 189957, 189958, 189959,
       189966, 189968, 189969, 189971, 189973, 189974, 189975, 189982,
       190002, 190009, 190010, 190011, 190013, 198914, 198922, 198924,
       198925, 198927, 198944, 198952, 198953, 198955, 198960, 198961,
       198963, 198965, 198972, 198974, 198975, 199120, 199121, 199123,
       199126, 199134
DEEP2-3   352.312  -0.433
       188485, 188488, 188490, 188491, 188492, 188513, 188516, 188517,
       188518, 188519, 188524, 188526, 188527, 188532, 188533, 188534,
       188535, 188538, 188540, 188542, 188543, 196740, 196743, 196754,
       196760, 196761, 196762, 196763, 196765, 196792, 196793, 196795,
       188484, 188486, 188487, 188489, 188493, 188494, 188495, 188512,
       188514, 188515, 188521, 188522, 188523, 188525, 188529, 188530,
       188531, 188536, 188537, 188539, 188541, 196741, 196742, 196748,
       196750, 196751, 196752, 196753, 196755, 196757, 196764, 196766,
       196767, 196786, 196794, 196796, 196797, 196799


Astrometry.net format
---------------------

The files here are in the new LSST catalog format, indexed by HTM, but can be
converted to the format used by Astrometry.net using the 'buildAndCatalog.py'
script, e.g.:

    buildAndCatalog.py -j 8 -o /path/to/output/ps1_pv3_3pi_20170110 '*.fits'

buildAndCatalog.py converts the coordinates from radians to degrees,
re-indexes by HEALPix (which allows Astrometry.net to quickly identify the
relevant files) and generates the Astrometry.net indices.  It can be run in
parallel (except for the re-indexing part, of which only one instance may run)
with the '-j' argument.

If you need to harness more CPU power than a single node can provide, you can
have buildAndCatalog.py use the LSST ctrl_pool package:

    mpiexec -n 8 python `which buildAndCatalog.py` --use-ctrl-pool -o /path/to/output/ps1_pv3_3pi_20170110 '*.fits'

Here's an example Slurm submission script:

    #!/bin/bash
    #SBATCH --ntasks=96
    #SBATCH --time=12:00:00
    #SBATCH --job-name=andIndex
    #SBATCH --dependency=singleton
    #SBATCH --output=/tigress/HSC/users/price/ps1_pv3/andIndex.o%j
    #SBATCH --error=/tigress/HSC/users/price/ps1_pv3/andIndex.o%j
    unset EUPS_DIR EUPS_SHELL EUPS_PATH EUPS_PKGROOT SETUP_EUPS
    . /tigress/HSC/LSST/stack_20160915/eups/bin/setups.sh
    setup lsst_distrib
    setup miniconda2
    export PYTHONPATH=/tigress/HSC/users/price/ps1_pv3/python/:$PYTHONPATH
    export PATH=/tigress/HSC/users/price/ps1_pv3/bin/:/tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422/DATA/ref_cats/ps1_pv3_3pi_20170110/bin:$PATH
    cd /tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422/DATA/ref_cats/ps1_pv3_3pi_20170110
    date
    mpiexec -bind-to socket python /tigress/HSC/users/price/ps1_pv3/3pi.pv3.20160422/DATA/ref_cats/ps1_pv3_3pi_20170110/bin/buildAndCatalog.py --use-ctrl-pool -o /tigress/HSC/users/price/ps1_pv3/ps1_pv3_3pi_20170110-and/ps1_pv3_3pi_20170110 '*.fits'
    date

Astrometry.net catalogs for specific regions could be built by supplying only
the HTM index files for that region instead of '*.fits'.

