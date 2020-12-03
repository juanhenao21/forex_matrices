'''HIST data main module.

The functions in the module compute the eigenvectors from correlation matrices
of the Historic Rate data from HIST Capital in different time intervals.

This script requires the following modules:
    * itertools
    * multiprocessing
    * typing
    * hist_data_analysis_eigenvectors_physical
    * hist_data_plot_eigenvectors_physical
    * hist_data_tools_eigenvectors_physical

The module contains the following functions:
    * hist_data_plot_generator - generates all the analysis and plots from the
      HIST data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
from typing import List

import hist_data_analysis_eigenvectors_physical
import hist_data_plot_eigenvectors_physical
import hist_data_tools_eigenvectors_physical

# -----------------------------------------------------------------------------


def hist_data_plot_generator(years: List[str], intervals: List[str]) -> None:
    """Generates all the analysis and plots from the HIST data.

    :param fx_pairs: list of the string abbreviation of the forex pairs to be
     analyzed (i.e. ['eur_usd', 'gbp_usd']).
    :param years: list of the string of the year to be analyzed
     (i.e. ['2016', '2017']).
    :param intervals: list of string of the interval to be analyzed
     (i.e. ['week', 'month', 'quarter', 'year'])
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:
        # Basic functions
        pool.starmap(hist_data_analysis_eigenvectors_physical
                     .hist_fx_eigenvectors_physical_data,
                     iprod(years, intervals))

    # Specific functions
    year: str
    for year in years:

        interval: str
        for interval in intervals:

            hist_data_plot_eigenvectors_physical. \
                hist_fx_eigenvectors_physical_plot(year, interval)


# -----------------------------------------------------------------------------


def main() -> None:
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    hist_data_tools_eigenvectors_physical.hist_initial_message()

    # Forex pairs and weeks to analyze
    # Response function analysis
    # The other years will be downloaded with the spread data
    years: List[str] = ['2019']
    intervals: List[str] = ['week', 'month', 'quarter', 'year']

    # Basic folders
    hist_data_tools_eigenvectors_physical.hist_start_folders(years)

    # Run analysis
    # Analysis and plot
    hist_data_plot_generator(years, intervals)

    print('Ay vamos!!!')

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
