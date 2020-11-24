'''HIST data analysis module.

The functions in the module compute the response function in trade time scale
from the Historic Rate Data from HIST Capital data in a year.

This script requires the following modules:
    * os
    * pickle
    * typing
    * numpy
    * pandas

The module contains the following functions:
    * hist_fx_correlations_physical_data - computes the correlation matrices
      for different time intervals.
    * hist_fx_returns-year_physical_data - concatenates the returns of a year
    * main - the main function of the script.

..moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''
# -----------------------------------------------------------------------------
# Modules

import os
import pickle
from typing import List, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

import hist_data_tools_matrices_physical

# -----------------------------------------------------------------------------


def hist_fx_returns_year_physical_data(fx_pairs: List[str], year: str) -> None:
    """Concatenates the returns of a year for different forex pairs.

    :param fx_pairs: list of the string abbreviation of the forex pairs to be
     analyzed (i.e. ['eur_usd', 'gbp_usd']).
    :param year: string of the year to be analyzed (i.e. '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    weeks: Tuple[str, ...] = hist_data_tools_matrices_physical.hist_weeks()

    try:

        fx_df_concat: pd.DataFrame = pd.DataFrame()

        fx_pair: str
        for fx_pair in fx_pairs:
            # Load first week data
            fx_data: pd.DataFrame = pickle.load(open(
                            f'../../hist_data/physical_basic_data_{year}/hist'
                            + f'_fx_physical_basic_data/{fx_pair}/hist_fx'
                            + f'_physical_basic_data_{fx_pair}_w01.pickle',
                            'rb'))
            fx_series_concat = fx_data['Returns']

            week: str
            for week in weeks[1:]:
                # Load data
                fx_data= pickle.load(open(
                            f'../../hist_data/physical_basic_data_{year}/'
                            + f'hist_fx_physical_basic_data/{fx_pair}/hist'
                            + f'_fx_physical_basic_data_{fx_pair}_w{week}'
                            + f'.pickle', 'rb'))

                fx_series_concat = pd.concat([fx_series_concat,
                                              fx_data['Returns']])

            fx_df_concat = pd.concat([fx_df_concat, fx_series_concat], axis=1)\
                             .rename(columns={'Returns': fx_pair})

        if (not os.path.isdir(
                f'../../hist_data/matrices_physical_{year}/hist_fx_matrices'
                + f'_physical_data/')):

            try:
                os.mkdir(
                    f'../../hist_data/matrices_physical_{year}/hist_fx'
                    + f'_matrices_physical_data/')
                print('Folder to save data created')

            except FileExistsError:
                print('Folder exists. The folder was not created')

        pickle.dump(fx_df_concat, open(
                        f'../../hist_data/matrices_physical_{year}/hist_fx'
                        + f'_matrices_physical_data/hist_fx_returns_matrices'
                        + f'_physical_data_{year}.pickle', 'wb'))

        del fx_data
        del fx_series_concat
        del fx_df_concat

    except FileNotFoundError as error:
        print('No data')
        print(error)
        print()

# -----------------------------------------------------------------------------


def hist_fx_correlations_physical_data(year: str, interval: str) -> None:
    """Computes the correlation matrix in an interval of time.

    :param year: string of the year to be analyzed (i.e. '2016').
    :param interval:
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    try:
        # Load data
        fx_returns: pd.DataFrame = pickle.load(open(
                        f'../../hist_data/matrices_physical_{year}/hist_fx'
                        + f'_matrices_physical_data/hist_fx_returns_matrices'
                        + f'_physical_data_{year}.pickle', 'rb'))

        corr = fx_returns.corr()

        del fx_returns

    except FileNotFoundError as error:
        print('No data')
        print(error)
        print()

# ----------------------------------------------------------------------------


def main() -> None:
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
