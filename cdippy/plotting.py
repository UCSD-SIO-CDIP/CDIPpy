from . import plots
from matplotlib.pyplot import Figure


def make_annual_hs_boxplot(stn: str, year: int) -> Figure:
    """
    Create a boxplot of annual significant wave heights for a given station and year.

    Parameters
    ----------
    stn : str
        A 5-character station identifier, e.g., '100p1'.
    year : int
        The year for which the boxplot is generated.

    Returns
    -------
    fig : Figure
        A matplotlib Figure object representing the annual wave height boxplot.

    Example
    -------
    >>> fig = make_annual_hs_boxplot('100p1', 2023)
    >>> fig.show()
    """
    return plots.annual_hs_boxplot.make_plot(stn, year)


def make_compendium_plot(
    stns: str, start: str, end: str, params: str, x_inch: int
) -> Figure:
    """
    Generate CDIP's classic compendium plot for multiple stations and parameters over a time range.

    Parameters
    ----------
    stns : str
        Comma-delimited list of 5-character station identifiers, e.g., '100p1,201p1'.
    start : str
        Start time formatted as 'yyyymm[ddHHMMss]'; optional components default to zero.
    end : str
        End time formatted as 'yyyymm[ddHHMMss]'. If None, defaults to current date/time.
    params : str
        Comma-delimited string of parameter names, e.g., 'waveHs,waveTp'.
    x_inch : int
        Width of the figure in inches.

    Returns
    -------
    fig : Figure
        A matplotlib Figure object representing the compendium plot.

    Example
    -------
    >>> fig = make_compendium_plot('100p1,201p1', '202301', '202312', 'waveHs,waveTp', 10)
    >>> fig.show()
    """
    return plots.compendium.make_plot(stns, start, end, params, x_inch)


def make_sst_climatology_plot(
    stn: str, x_inch: int = None, y_inch: int = None
) -> Figure:
    """
    Plot the yearly climatology of sea surface temperature for a given station over all available years.

    Parameters
    ----------
    stn : str
        A 5-character station identifier, e.g., '100p1'.
    x_inch : int, optional
        Width of the figure in inches. Default is None.
    y_inch : int, optional
        Height of the figure in inches. Default is None.

    Returns
    -------
    fig : Figure
        A matplotlib Figure object representing the SST climatology plot.

    Example
    -------
    >>> fig = make_sst_climatology_plot('100p1', x_inch=8, y_inch=6)
    >>> fig.show()
    """
    return plots.sst_climatology.make_plot(stn, x_inch, y_inch)
