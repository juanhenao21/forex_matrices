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
    * hist_fx_self_response_week_responses_physical - extracts the midpoint
      price for a week.
    * hist_fx_self_response_year_responses_physical - extracts the midpoint
      price for a year.
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

import hist_data_tools_responses_physical

__tau__ = 10000

# -----------------------------------------------------------------------------


def hist_fx_self_response_week_responses_physical_data(
        fx_pair: str, year: str, week: str) -> Tuple[np.ndarray, ...]:
    """Computes the self-response of a year.

    Using the midpoint price and the trade signs of a ticker computes the
    self-response during different time lags (:math:`\\tau`) for a year.

    :param fx_pair: string of the abbreviation of the forex pair to be analyzed
     (i.e. 'eur_usd').
    :param year: string of the year to be analyzed (i.e. '2016').
    :param week: string of the week to be analyzed (i.e. '01').
    :return: tuple -- The function returns a tuple with numpy arrays.
    """

    try:
        # Load data
        fx_data: pd.DataFrame = pickle.load(open(
                        f'../../hist_data/physical_basic_data_{year}/hist_fx'
                        + f'_physical_basic_data/{fx_pair}/hist_fx_physical'
                        + f'_basic_data_{fx_pair}_w{week}.pickle', 'rb'))

        midpoint: np.ndarray = fx_data['Midpoint'].to_numpy()
        trade_signs: np.ndarray = fx_data['Signs'].to_numpy()

        # Relate the return of the previous second with the current trade sign
        midpoint = midpoint[:-1]
        trade_signs = trade_signs[1:]

        assert len(midpoint) == len(trade_signs)

        # Array of the average of each tau
        self_response_tau: np.ndarray = np.zeros(__tau__)
        num: np.ndarray = np.zeros(__tau__)

        # Calculating the midpoint price return and the self-response function
        # Depending on the tau value
        tau_idx: int
        for tau_idx in range(__tau__):

            trade_sign_tau: np.ndarray = trade_signs[:-tau_idx - 1]
            trade_sign_no_0_len: int = len(trade_sign_tau[trade_sign_tau != 0])
            num[tau_idx] = trade_sign_no_0_len
            # Obtain the midpoint price return. Displace the numerator tau
            # values to the right and compute the return

            # Midpoint price returns
            log_return_sec: np.ndarray = (midpoint[tau_idx + 1:]
                                          - midpoint[:-tau_idx - 1]) \
                / midpoint[:-tau_idx - 1]

            # Obtain the self response value
            if trade_sign_no_0_len != 0:
                product: np.ndarray = log_return_sec * trade_sign_tau
                self_response_tau[tau_idx] = np.sum(product)

        del fx_data

        return (self_response_tau, num)

    except FileNotFoundError as error:
        print('No data')
        print(error)
        print()
        zeros = np.zeros(__tau__)
        return (zeros, zeros)

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

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
