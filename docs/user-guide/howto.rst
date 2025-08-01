.. include:: ../references.txt

.. _how_to:

How To
======

This page contains short "how to" or "frequently asked question" entries for
Gammapy. Each entry is for a very specific task, with a short answer, and links
to examples and documentation.

If you're new to Gammapy, please check the :ref:`getting-started` section and
the :ref:`user_guide` and have a look at the list of :ref:`tutorials`.
The information below is in addition to those pages, it's not a complete list of
how to do everything in Gammapy.

Please give feedback and suggest additions to this page!


.. dropdown:: Spell and pronounce Gammapy

    The recommended spelling is "Gammapy" as proper name. The recommended
    pronunciation is [ɡæməpaɪ] where the syllable "py" is pronounced like
    the english word "pie". You can listen to it `here <http://ipa-reader.xyz/?text=ˈ%C9%A1æməpaɪ&voice=Amy>`__.


.. dropdown:: Select observations

    The `~gammapy.data.DataStore` provides access to a summary table of all observations available.
    It can be used to select observations with various criterion. You can for instance apply a cone search
    or also select observations based on other information available using the
    `~gammapy.data.ObservationTable.select_observations` method.

    .. button-link:: ../tutorials/starting/analysis_2.html#defining-the-datastore-and-selecting-observations
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Make observation duration maps

    Gammapy offers a number of methods to explore the content of the various IRFs
    contained in an observation. This is usually done thanks to their ``peek()``
    methods.

    .. button-link:: ../tutorials/details/makers.html#observation-duration-and-effective-livetime
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Group observations

    `~gammapy.data.Observations` can be grouped depending on a number of various quantities.
    The two methods to do so are manual grouping and hierarchical clustering. The quantity
    you group by can be adjusted according to each science case.

    .. button-link:: ../tutorials/details/observation_clustering.html
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Make an on-axis equivalent livetime map

    The `~gammapy.data.DataStore` provides access to a summary table of all observations available.
    It can be used to obtain various quantities from your `~gammapy.data.Observations` list, such as livetime.
    The on-axis equivalent number of observation hours on the source can be calculated.

    .. button-link:: ../tutorials/details/makers.html#observation-duration-and-effective-livetime
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Compute minimum number of counts of significance per bin

    The `~gammapy.estimators.utils.resample_energy_edges` provides a way to resample the energy bins
    to satisfy a minimum number of counts of significance per bin.

    .. button-link:: ../tutorials/analysis-1d/spectral_analysis.html#compute-flux-points
       :color: primary
       :shadow:

       To the tutorial...



.. dropdown:: Choose units for plotting

    Units for plotting are handled with a combination of `matplotlib` and `astropy.units`.
    The methods `ax.xaxis.set_units()` and `ax.yaxis.set_units()` allow
    you to define the x and y axis units using `astropy.units`. Here is a minimal example:

    .. code::

        import matplotlib.pyplot as plt
        from gammapy.estimators import FluxPoints
        from astropy import units as u

        filename = "$GAMMAPY_DATA/hawc_crab/HAWC19_flux_points.fits"
        fp = FluxPoints.read(filename)

        ax = plt.subplot()
        ax.xaxis.set_units(u.eV)
        ax.yaxis.set_units(u.Unit("erg cm-2 s-1"))
        fp.plot(ax=ax, sed_type="e2dnde")


.. dropdown:: Compute the significance of a source

    Estimating the significance of a source, or more generally of an additional model
    component (such as e.g. a spectral line on top of a power-law spectrum), is done
    via a hypothesis test. You fit two models: one including the source or component and one without it. Then,
    compute the difference in the test statistic (TS) between the two fits to determine the
    significance or p-value. To obtain the test statistic, call
    `~gammapy.modeling.Dataset.stat_sum` for the model corresponding to your two
    hypotheses (or take this value from the print output when running the fit), and
    take the difference. Note that in Gammapy, the fit statistic is defined as
    :math:`S = - 2 * log(L)` for likelihood :math:`L`, such that :math:`TS = S_0 - S_1`. See
    :ref:`datasets` for an overview of fit statistics used.



.. dropdown:: Perform data reduction loop with multi-processing

    There are two ways for the data reduction steps to be implemented. Either a loop is used to
    run the full reduction chain, or the reduction is performed with multi-processing tools by
    utilising the `~gammapy.makers.DatasetsMaker` to perform the loop internally.

    .. button-link:: ../tutorials/details/makers.html#data-reduction-loop
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Compute cumulative significance over time

    A classical plot in gamma-ray astronomy is the cumulative significance of a
    source as a function of observing time. In Gammapy, you can produce it with 1D
    (spectral) analysis. Once datasets are produced for a given ON region, you can
    access the total statistics with the ``info_table(cumulative=True)`` method of
    `~gammapy.datasets.Datasets`.

    .. button-link:: ../tutorials/analysis-1d/spectral_analysis.html#source-statistic
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Implement a custom model

    Gammapy allows the flexibility of using user-defined models for analysis.

    .. button-link:: ../tutorials/details/models.html#implementing-a-custom-model
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Implement energy dependent spatial models

    While Gammapy does not ship energy dependent spatial models, it is possible to define
    such models within the modeling framework.

    .. button-link:: ../tutorials/details/models.html#models-with-energy-dependent-morphology
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Model astrophysical source spectra

    It is possible to combine Gammapy with astrophysical modeling codes, if they
    provide a Python interface. Usually this requires some glue code to be written,
    e.g. `~gammapy.modeling.models.NaimaSpectralModel` is an example of a Gammapy
    wrapper class around the Naima spectral model and radiation classes, which then
    allows modeling and fitting of Naima models within Gammapy (e.g. using CTAO,
    H.E.S.S. or Fermi-LAT data).


.. dropdown:: Model temporal profiles

    Temporal models can be directly fit on available lightcurves,
    or on the reduced datasets. This is done through a joint fitting of the datasets,
    one for each time bin.

    .. button-link:: ../tutorials/analysis-time/light_curve_simulation.html#fitting-temporal-models
       :color: primary
       :shadow:

       To the tutorial...


.. dropdown:: Improve fit convergence with constraints on the source position

    It happens that a 3D fit does not converge with warning messages indicating that the
    scanned positions of the model are outside the valid IRF map range. The type of warning message is:
    ::

        Position <SkyCoord (ICRS): (ra, dec) in deg
        (329.71693826, -33.18392464)> is outside valid IRF map range, using nearest IRF defined within

    This issue might happen when the position of a model has no defined range. The minimizer
    might scan positions outside the spatial range in which the IRFs are computed and then it gets lost.

    The simple solution is to add a physically-motivated range on the model's position, e.g. within
    the field of view or around an excess position. Most of the time, this tip solves the issue.
    The documentation of the :ref:`models sub-package <modifying-model-parameters>`
    explains how to add a validity range of a model parameter.


.. dropdown:: Reduce memory budget for large datasets

    When dealing with surveys and large sky regions, the amount of memory required might become
    problematic, in particular because of the default settings of the IRF maps stored in the
    `~gammapy.datasets.MapDataset` used for the data reduction. Several options can be used to reduce
    the required memory:
    - Reduce the spatial sampling of the `~gammapy.irf.PSFMap` and the `~gammapy.irf.EDispKernelMap`
    using the `binsz_irf` argument of the `~gammapy.datasets.MapDataset.create` method. This will reduce
    the accuracy of the IRF kernels used for model counts predictions.
    - Change the default IRFMap axes, in particular the `rad_axis` argument of `~gammapy.datasets.MapDataset.create`
    This axis is used to define the geometry of the `~gammapy.irf.PSFMap` and controls the distribution of error angles
    used to sample the PSF. This will reduce the quality of the PSF description.
    - If one or several IRFs are not required for the study at hand, it is possible not to build them
    by removing it from the list of options passed to the `~gammapy.makers.MapDatasetMaker`.


.. dropdown:: Copy part of a data store

    To share specific data from a database, it might be necessary to create a new data storage with
    a limited set of observations and summary files following the scheme described in gadf_.
    This is possible with the method `~gammapy.data.DataStore.copy_obs` provided by the
    `~gammapy.data.DataStore`. It allows to copy individual observations files in a given directory
    and build the associated observation and HDU tables.


.. dropdown:: Interpolate onto a different geometry

    To interpolate maps onto a different geometry use `~gammapy.maps.Map.interp_to_geom`.

    .. button-link:: ../tutorials/details/maps.html#filling-maps-from-interpolation
       :color: primary
       :shadow:

       To the tutorial...

.. dropdown:: Suppress warnings

    In general it is not recommended to suppress warnings from code because they
    might point to potential issues or help debugging a non-working script. However
    in some cases the cause of the warning is known and the warnings clutter the
    logging output. In this case it can be useful to locally suppress a specific
    warning like so:

    .. testcode::

        from astropy.io.fits.verify import VerifyWarning
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', VerifyWarning)
            # do stuff here


.. dropdown:: Avoid NaN results in Flux Point estimation

    Sometimes, upper limit values may show as ``nan`` while running a `~gammapy.estimators.FluxPointsEstimator`
    or a `~gammapy.estimators.LightCurveEstimator`. This likely arises because the min/max range of the `norm` parameter
    attribute attached to the estimator is not well-chosen (the automatic default may not be valid for all use cases).
    Setting these min/max to large values usually solves the problem (see the attributes of `norm`
    `~gammapy.modeling.Parameter`). In some cases, you can also consider configuring the estimator with a different
    `~gammapy.modeling.Fit` backend.

    .. button-link:: ../tutorials/details/estimators.html#a-fully-configured-flux-points-estimatio
       :color: primary
       :shadow:

       To the tutorial...

.. dropdown:: Display a progress bar

    Gammapy provides the possibility of displaying a
    progress bar to monitor the advancement of time-consuming processes. To activate this
    functionality, make sure that `tqdm` is installed and add the following code snippet
    to your code:

    .. testcode::

        from gammapy.utils import pbar
        pbar.SHOW_PROGRESS_BAR = True

    The progress bar is available within the following:

    * `~gammapy.data.DataStore.get_observations` method

    * The ``run()`` method from the ``estimator`` classes: `~gammapy.estimators.ASmoothMapEstimator`, `~gammapy.estimators.TSMapEstimator`, `~gammapy.estimators.LightCurveEstimator`

    * `~gammapy.modeling.Fit.stat_profile` and `~gammapy.modeling.Fit.stat_surface` methods

    * `~gammapy.scripts.download.progress_download` method

    * `~gammapy.utils.parallel.run_multiprocessing` method


.. dropdown:: Change plotting style and color-blind friendly visualizations

    As the Gammapy visualisations are using the library `matplotlib` that provides color styles,
    it is possible to change the default colors map of the Gammapy plots. Using using the
    `style sheet of matplotlib <https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html>`_,
    you should add into your notebooks or scripts the following lines after the Gammapy imports:

    .. code::

        import matplotlib.style as style
        style.use('XXXX')
        # with XXXX from `print(plt.style.available)`

    Note that you can create your own style with matplotlib (see
    `here <https://matplotlib.org/stable/tutorials/introductory/customizing.html>`__ and
    `here <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`__)

    The CTAO observatory released a document describing best practices for **data
    visualisation in a way friendly to color-blind people**:
    `CTAO document <https://www.ctao.org/wp-content/uploads/ColourBlindFriendlyPractices_v2_032025.pdf>`_.
    To use them, you should add into your notebooks or scripts the following lines after the Gammapy imports:

    .. code::

        import matplotlib.style as style
        style.use('tableau-colorblind10')

    or

    .. code::

        import matplotlib.style as style
        style.use('seaborn-colorblind')


.. dropdown:: Add PHASE information to your data

    To do a pulsar analysis, one must compute the pulsar phase of
    each event and put this new information in a new `~gammapy.data.Observation`.
    Computing pulsar phases can be done using an external library such as
    `PINT <https://nanograv-pint.readthedocs.io/en/latest/>`__ or
    `Tempo2 <https://www.pulsarastronomy.net/pulsar/software/tempo2>`__. A
    gammapy recipe showing how to use PINT within the Gammapy framework is available
    `here <https://gammapy.github.io/gammapy-recipes/_build/html/notebooks/pulsar_phase/pulsar_phase_computation.html>`__.
    For brevity, the code below shows how to add a dummy phase column to a new
    `~gammapy.data.EventList` and `~gammapy.data.Observation`.

    .. testcode::

        import numpy as np
        from gammapy.data import DataStore, Observation, EventList

        # read the observation
        datastore = DataStore.from_dir("$GAMMAPY_DATA/hess-dl3-dr1/")
        obs = datastore.obs(23523)

        # use the phase information - dummy in this example
        phase = np.random.random(len(obs.events.table))

        # create a new `EventList`
        table = obs.events.table
        table["PHASE"] = phase
        new_events = EventList(table)

        # copy the observation in memory, changing the events
        obs2 = obs.copy(events=new_events, in_memory=True)

        # The new observation and the new events table can be serialised independently
        obs2.write("new_obs.fits.gz", overwrite=True)
        obs2.write("events.fits.gz", include_irfs=False, overwrite=True)


