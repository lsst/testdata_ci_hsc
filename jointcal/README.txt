This directory contains jointcal results for the ci_hsc dataset.

We don't run jointcal as part of ci_hsc, because it needs a full focal plane
to get decent results. Instead, we've run it separately, and dumped the results
here. This allows us to check that the mechanics of applying the jointcal
results works.


singleFrameDriver.py /projects/HSC/HSC --calib /projects/HSC/HSC/CALIB-LSST-20170105 --rerun price/dm-20841-ci_hsc --id visit=903334^903336^903338^903342^903344^903346 --job ci_hsc-r --time 600 --cores 112 --batch-type=slurm --batch-submit='--mem-per-cpu 4000' --mpiexec='-bind-to socket'
singleFrameDriver.py /projects/HSC/HSC --calib /projects/HSC/HSC/CALIB-LSST-20170105 --rerun price/dm-20841-ci_hsc --id visit=903986^903988^903990^904010^904014 --job ci_hsc-i --time 600 --cores 112 --batch-type=slurm --batch-submit='--mem-per-cpu 4000' --mpiexec='-bind-to socket'

makeSkyMap.py /projects/HSC/HSC --calib /projects/HSC/HSC/CALIB-LSST-20170105 --rerun price/dm-20841-ci_hsc -C /tigress/pprice/ci_hsc_gen2/skymap.py

jointcal.py /projects/HSC/HSC --calib /projects/HSC/HSC/CALIB-LSST-20170105 --rerun price/dm-20841-ci_hsc --id tract=0 visit=903334^903336^903338^903342^903344^903346 ccd=0..103
jointcal.py /projects/HSC/HSC --calib /projects/HSC/HSC/CALIB-LSST-20170105 --rerun price/dm-20841-ci_hsc --id tract=0 visit=903986^903988^903990^904010^904014 ccd=0..103


scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903334-016.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903334-022.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903334-023.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903334-100.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903336-017.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903336-024.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903338-018.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903338-025.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903342-004.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903342-010.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903342-100.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903344-000.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903344-005.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903344-011.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903346-001.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903346-006.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903346-012.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903986-016.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903986-022.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903986-023.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903986-100.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0904014-001.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0904014-006.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0904014-012.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903990-018.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903990-025.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0904010-004.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0904010-010.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0904010-100.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903988-016.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903988-017.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903988-023.fits .
scp tiger:/projects/HSC/HSC/rerun/price/dm-20841-ci_hsc/jointcal-results/*/0000/jointcal_*-0903988-024.fits .

Finally, we convert to the gen3-compatible ExposureCatalogs:

python ./convert_ci_hsc_jointcal_to_exposurecatalogs.py
