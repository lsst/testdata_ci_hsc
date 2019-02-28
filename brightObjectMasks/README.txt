The bright object masks for the custom skymap in ci_hsc were provided by
Andy Goulding <goulding@astro.princeton.edu>, who writes:

> The new star masks for S18A based upon GAIA DR2 are now finished. There are
> individual masks for each of the g,r,i,z,y filters.
> 
> I have spent a substantial amount of time testing the masks in the Hectomap
> region. I found that the g-band suffers from an additional extended low-level
> component that I could not find significant evidence for in the other filters.
> However, when I attempted to fully mask this additional component we lost a
> substantial fraction of the survey area (>80%) -- this did not seem
> acceptable, and I made the decision that this component should not be included
> in the g-band mask. I think a caution in the data release notes for source
> selections that are entirely based on g-band magnitude should suffice. I also
> noticed strange asymmetric arcs around some of the bright stars in the y-band.
> These only showed up around some bright stars and they were not consistent in
> their position around the stars. Simply looking at the density of detected
> sources did not allow me to determine when this feature would and wouldn’t
> appear, and so it is also not included in the mask — it’s relatively narrow,
> and so ultimately it may be a negligible issue anyway.
> 
> The relation between (log) star radius and the star brightness was found to be
> very close to linear in each filter (with the exception of the g-band; see
> above) such that:
>    log(radius [degrees]) = a + b*gaia_Gmag
> The best fit in each filter was determined based on the density of bright HSC
> sources as a function of radius from each star. Within the uncertainties, the
> gradient was found to be identical for each filter, and so for simplicity I
> fixed it to the median gradient found for each filter with b = -0.146
> The filter-dependent normalizations were determined to be
> a={+0.01, +0.01, -0.01, -0.05, -0.03} for g,r,i,z,y respectively. While the
> difference between the mask size in the individual filters is only at the
> ~10% level, overall, the masks are still significantly larger than the
> arcturus mask [i.e., the previous version, provided by Jean Coupon]. This
> larger mask is required to account for the extended halos of bright
> (20-24 mag) "detected sources” around star positions that are in the S18A
> catalog. I’m not going to make the claim that these new masks are perfect,
> but I do believe that they provide a useful fix for the current source catalog
> that will allow science to be performed using the S18A database.
