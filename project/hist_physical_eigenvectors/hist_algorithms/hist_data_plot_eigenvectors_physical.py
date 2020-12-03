'''HIST data plot module.

The functions in the module plot the data obtained in the
hist_data_analysis_eigenvectors_physical module.

This script requires the following modules:
    * gc
    * pickle
    * matplotlib
    * numpy
    * pandas
    * seaborn
    * hist_data_tools_data_extract

The module contains the following functions:
    * hist_fx_eigenvectors_physical_plot - plots the eigenvectors of
      correlation matrices for different time intervals.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

import gc
import pickle

from matplotlib import pyplot as plt  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import seaborn as sns  # type: ignore

import hist_data_tools_eigenvectors_physical

# -----------------------------------------------------------------------------


def hist_fx_eigenvectors_physical_plot(year: str, interval: str) -> None:
    """Plots the eigenvectors of correlation matrices.

    :param year: string of the year to be analyzed (i.e. '2016').
    :param interval: string of the interval to be analyzed (i.e. 'week',
     'month', 'quarter', 'year')
    :return: None -- The function saves the plot in a file and does not return
     a value.
    """

    function_name: str = \
        hist_fx_eigenvectors_physical_plot.__name__
    hist_data_tools_eigenvectors_physical \
        .hist_function_header_print_plot(function_name, year)

    try:

        periods: int
        n_cols: int
        n_rows: int
        if interval == 'week':
            periods = 52
            n_cols = 13
            n_rows = 4
        elif interval == 'month':
            periods = 12
            n_cols = 4
            n_rows = 3
        elif interval == 'quarter':
            periods = 4
            n_cols = 2
            n_rows = 2
        else:
            periods = 1
            n_cols = 1
            n_rows = 1

        figure: plt.figure = plt.figure(figsize=(16, 9))
        cbar_ax: plt.axes = figure.add_axes([0.91, 0.3, 0.03, 0.4])

        for per in range(1, periods + 1):

            if per < 10:
                per_str: str = f'0{per}'
            else:
                per_str = f'{per}'

            # Load data
            eigenvectors: pd.DataFrame = pickle.load(open(
                f'../../hist_data/eigenvectors_physical_{year}/hist_fx_eigenvectors'
                + f'_physical_data/hist_fx_eigenvectors_physical_data_{year}_int'
                + f'_{interval}_{per_str}.pickle', 'rb'))

            ax_sub = plt.subplot(n_rows, n_cols, per)

            if interval in ('week', 'month'):
                sns.heatmap(eigenvectors, ax=ax_sub, cbar=per == 1,
                            cbar_ax=None if (per-1) else cbar_ax,
                            vmin=-1, vmax=1)

            else:
                sns.heatmap(eigenvectors, annot=True, ax=ax_sub, cbar=per == 1,
                            cbar_ax=None if (per-1) else cbar_ax,
                            vmin=-1, vmax=1)

            if interval == 'week':
                ax_sub.tick_params(axis='x', bottom=False, labelbottom=False)
                ax_sub.tick_params(axis='y', left=False, labelleft=False)

            plt.yticks(rotation=45)
            plt.xticks(rotation=45)

        figure.tight_layout(rect=[0, 0, .9, 1])

        # Plotting
        hist_data_tools_eigenvectors_physical \
            .hist_save_plot(function_name, figure, year, interval)

        plt.close()
        del eigenvectors
        del figure
        gc.collect()

    except FileNotFoundError as error:
        print('No data')
        print(error)
        print()

# -----------------------------------------------------------------------------


def main() -> None:
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    hist_fx_eigenvectors_physical_plot('2019', 'year')

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
