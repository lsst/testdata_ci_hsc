# We haven't processed all the patches that overlap some of our CCDs
# to save some time.
config.references.skipMissing = True

# CModel doesn't yet implement forced photometry when WCSs differ,
# so we disable it here (and reset the classification parameters
# to use GaussianFlux).
config.measurement.plugins.names.discard("modelfit_CModel")
config.measurement.slots.modelFlux = "base_GaussianFlux"
config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio = 0.925
