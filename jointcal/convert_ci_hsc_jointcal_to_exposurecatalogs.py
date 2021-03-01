import lsst.afw.table
import lsst.afw.image
import lsst.afw.geom
import lsst.daf.base
import glob
import os
import re


def convert():
    jointcalDir = os.path.join(os.environ['TESTDATA_CI_HSC_DIR'], 'jointcal')

    # We sort the files to group by visit
    photoCalibFiles = sorted(glob.glob(os.path.join(jointcalDir, 'jointcal_photoCalib-*.fits')))
    wcsFiles = sorted(glob.glob(os.path.join(jointcalDir, 'jointcal_wcs-*.fits')))

    # Extract the visit and detector from the filename.
    photoCalibMap = {}
    for photoCalibFile in photoCalibFiles:
        matches = re.search(r'photoCalib-(\d+)-(\d+)\.fits', photoCalibFile)
        photoCalibMap[photoCalibFile] = (int(matches.groups()[0]),
                                         int(matches.groups()[1]))

    wcsMap = {}
    for wcsFile in wcsFiles:
        matches = re.search(r'wcs-(\d+)-(\d+)\.fits', wcsFile)
        wcsMap[wcsFile] = (int(matches.groups()[0]),
                           int(matches.groups()[1]))

    # Make a schema.
    # We use the id field to set the detector_id and then sort that
    expCatalogSchema = lsst.afw.table.ExposureTable.makeMinimalSchema()
    expCatalogSchema.addField('visit', type='I', doc='Visit number')

    metadata = lsst.daf.base.PropertyList()
    metadata.add("COMMENT", "Catalog id is detector id, sorted.")
    metadata.add("COMMENT", "Only detectors with data have entries.")

    expCatalog = None
    lastVisit = None
    for photoCalibFile in photoCalibFiles:
        if photoCalibMap[photoCalibFile][0] != lastVisit:
            if expCatalog is not None:
                expCatalog.setMetadata(metadata)
                expCatalog.sort()  # Ensure that the detectors are sorted, for fast lookups.
                expCatalog.writeFits(f'jointcal_photoCalibCatalog-{lastVisit:07d}.fits')

            # Make a new expCatalog
            expCatalog = lsst.afw.table.ExposureCatalog(expCatalogSchema)
            lastVisit = photoCalibMap[photoCalibFile][0]

        rec = expCatalog.addNew()
        rec['visit'] = photoCalibMap[photoCalibFile][0]
        rec['id'] = photoCalibMap[photoCalibFile][1]

        photoCalib = lsst.afw.image.PhotoCalib.readFits(photoCalibFile)
        rec.setPhotoCalib(photoCalib)

    # And write out the last one
    expCatalog.setMetadata(metadata)
    expCatalog.sort()  # Ensure that the detectors are sorted, for fast lookups.
    expCatalog.writeFits(f'jointcal_photoCalibCatalog-{lastVisit:07d}.fits')

    expCatalog = None
    lastVisit = None
    for wcsFile in wcsFiles:
        if wcsMap[wcsFile][0] != lastVisit:
            if expCatalog is not None:
                expCatalog.setMetadata(metadata)
                expCatalog.sort()  # Ensure that the detectors are sorted, for fast lookups.
                expCatalog.writeFits(f'jointcal_wcsCatalog-{lastVisit:07d}.fits')

            # Make a new expCatalog
            expCatalog = lsst.afw.table.ExposureCatalog(expCatalogSchema)
            lastVisit = wcsMap[wcsFile][0]

        rec = expCatalog.addNew()
        rec['visit'] = wcsMap[wcsFile][0]
        rec['id'] = wcsMap[wcsFile][1]

        wcs = lsst.afw.geom.SkyWcs.readFits(wcsFile)
        rec.setWcs(wcs)

    # And write out the last one
    expCatalog.setMetadata(metadata)
    expCatalog.sort()  # Ensure that the detectors are sorted, for fast lookups.
    expCatalog.writeFits(f'jointcal_wcsCatalog-{lastVisit:07d}.fits')


if __name__ == '__main__':
    convert()
