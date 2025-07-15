# import plots library
from . import plots

# import public top-level modules
from . import cdipnc, nchashes, ncstats, ndbc, spectra, stndata

# public API (i.e. "from cdippy import *")
__all__ = ["plots", "cdipnc", "nchashes", "ncstats", "ndbc", "spectra", "stndata"]
