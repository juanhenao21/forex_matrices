'''HIST data analysis module.

The functions in the module compute the response function in trade time scale
from the Historic Rate Data from HIST Capital data in a year.

This script requires the following modules:
    * itertools
    * multiprocessing
    * os
    * pickle
    * typing
    * numpy
    * pandas

The module contains the following functions:
    * hist_fx_corr_physical - computes the correlation matrices for different
      time intervals.
    * main - the main function of the script.

..moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''
# -----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import os
import pickle
from typing import Iterator, List, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

import hist_data_tools_matrices_physical

# -----------------------------------------------------------------------------


def hist_fx_returns_year_physical_data(fx_pairs: List[str], year: str) -> None:
    """Concatenate the returns of a year for different forex pairs.

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
                            f'../../hist_data/physical_basic_data_{year}/hist_fx'
                            + f'_physical_basic_data/{fx_pair}/hist_fx_physical'
                            + f'_basic_data_{fx_pair}_w01.pickle', 'rb'))
            fx_series_concat = fx_data['Returns']

            week: str
            for week in weeks[1:]:
                # Load data
                fx_data: pd.DataFrame = pickle.load(open(
                                f'../../hist_data/physical_basic_data_{year}/hist_fx'
                                + f'_physical_basic_data/{fx_pair}/hist_fx_physical'
                                + f'_basic_data_{fx_pair}_w{week}.pickle', 'rb'))

                fx_series_concat = pd.concat([fx_series_concat, fx_data['Returns']])

            fx_df_concat = pd.concat([fx_df_concat, fx_series_concat], axis=1).rename(columns={'Returns': fx_pair})

        if (not os.path.isdir(
                f'../../hist_data/matrices_physical_{year}/hist_fx_matrices'
                + f'_physical_data/')):

            try:
                os.mkdir(
                    f'../../hist_data/matrices_physical_{year}/hist_fx_matrices'
                    + f'_physical_data/')
                print('Folder to save data created')

            except FileExistsError:
                print('Folder exists. The folder was not created')

        pickle.dump(fx_df_concat, open(f'../../hist_data/matrices_physical_{year}/hist_fx_matrices_physical_data/hist_fx_returns_matrices_physical_data_{year}.pickle', 'wb'))

        del fx_data
        del fx_series_concat
        del fx_df_concat

    except FileNotFoundError as error:
        print('No data')
        print(error)
        print()

# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns

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
                        + f'_matrices_physical_data/hist_fx_returns_matrices_physical'
                        + f'_data_{year}.pickle', 'rb'))

        corr = fx_returns.corr()

        sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)
        plt.show()


        del fx_returns


    except FileNotFoundError as error:
        print('No data')
        print(error)
        print()

# ----------------------------------------------------------------------------


def hist_fx_self_response_year_responses_physical_data(
        fx_pair: str, year: str) -> Tuple[np.ndarray, ...]:
    """Computes the self-response of a year.

    Using the hist_self_response_year_responses_physical_data function computes
    the self-response function for a year.

    :param ticker: string of the abbreviation of stock to be analyzed
     (i.e. 'AAPL').
    :param year: string of the year to be analyzed (i.e '2016').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    function_name: str = hist_fx_self_response_year_responses_physical_data \
        .__name__
    hist_data_tools_responses_physical \
        .hist_function_header_print_data(function_name, fx_pair, year, '')

    weeks: Tuple[str, ...] = hist_data_tools_responses_physical.hist_weeks()

    self_values: List[np.ndarray] = []
    args_prod: Iterator[Tuple[str, ...]] = iprod([fx_pair], [year], weeks)

    # Parallel computation of the self-responses. Every result is appended to
    # a list
    with mp.Pool(processes=mp.cpu_count()) as pool:
        self_values.append(pool.starmap(
            hist_fx_self_response_week_responses_physical_data, args_prod))

    # To obtain the total self-response, I sum over all the self-response
    # values and all the amount of trades (averaging values)
    self_v_final: np.ndarray = np.sum(self_values[0], axis=0)

    self_response_val: np.ndarray = self_v_final[0] / self_v_final[1]
    self_response_avg: np.ndarray = self_v_final[1]

    # Saving data
    if (not os.path.isdir(
            f'../../hist_data/responses_physical_{year}/{function_name}/')):

        try:
            os.mkdir(
                f'../../hist_data/responses_physical_{year}/{function_name}/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    if (not os.path.isdir(
            f'../../hist_data/responses_physical_{year}/{function_name}/'
            + f'{fx_pair}/')):

        try:
            os.mkdir(
                f'../../hist_data/responses_physical_{year}/{function_name}/'
                + f'{fx_pair}/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    hist_data_tools_responses_physical \
        .hist_save_data(self_response_val, fx_pair, year)

    return (self_response_val, self_response_avg)


# -----------------------------------------------------------------------------


def main() -> None:
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

    fx_pairs: List[str] = ['eur_usd', 'gbp_usd', 'usd_jpy', 'aud_usd',
                             'usd_chf', 'usd_cad', 'nzd_usd']

    # hist_fx_returns_year_physical_data(fx_pairs, ['2019'])

    hist_fx_correlations_physical_data('2019', 'x')

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
