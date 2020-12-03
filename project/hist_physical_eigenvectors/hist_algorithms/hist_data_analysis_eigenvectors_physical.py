'''HIST data analysis module.

The functions in the module compute the eigenvectors from correlation matrices
in physical time scale from the Historic Rate Data from HIST Capital data.

This script requires the following modules:
    * os
    * pickle
    * typing
    * pandas

The module contains the following functions:
    * hist_fx_eigenvectors_physical_data - computes the eigenvectors of
      correlation matrices for different time intervals.
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

import hist_data_tools_eigenvectors_physical

# -----------------------------------------------------------------------------


def hist_fx_eigenvectors_physical_data(year: str, interval: str) -> None:
    """Computes the eigenvectors of correlation matrix in an interval of time.

    :param year: string of the year to be analyzed (i.e. '2016').
    :param interval: string of the interval to be analyzed (i.e. 'week',
     'month', 'quarter', 'year')
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    function_name: str = hist_fx_eigenvectors_physical_data.__name__
    hist_data_tools_eigenvectors_physical \
        .hist_function_header_print_data(function_name, year)

    try:


        freq: str
        periods: int
        if interval == 'week':
            freq = 'W'
            periods = 52
        elif interval == 'month':
            freq = 'MS'
            periods = 12
        else:
            freq = 'QS'
            periods = 4

        if interval == 'year':
            # Load data
            fx_corr: pd.DataFrame = pickle.load(open(
                            f'../../hist_data/matrices_physical_{year}/hist_fx'
                            + f'_matrices_physical_data/hist_fx_corr_physical'
                            + f'_data_{year}_int_{interval}_01.pickle', 'rb'))

            print('Correlation Matrix')
            print()
            print(fx_corr)
            print()
            eig_val: np.ndarray
            eig_vec: np.ndarray
            eig_val, eig_vec = np.linalg.eig(fx_corr)
            # print(eig_val)

            eig_vec_sort = eig_vec[:, np.argsort(eig_val)[::-1]]
            print()
            print('Eigenvectors sorted according to the largest Eigenvalues')
            print()
            print(eig_vec_sort)
            # eig_vec_sort_df = pd.DataFrame(data=eig_vec_sort,
            #                                index=fx_corr.columns,
            #                                columns=fx_corr.columns)
            # print(eig_vec_sort_df)

            # hist_data_tools_eigenvectors_physical \
            #     .hist_save_data(corr, year, interval, '01')

        else:
            # Load data
            fx_returns: pd.DataFrame = pickle.load(open(
                            f'../../hist_data/matrices_physical_{year}/hist_fx'
                            + f'_matrices_physical_data/hist_fx_corr_physical_data'
                            + f'_{year}_int_{interval}_{t_idx}'
                            + f'_physical_data_{year}.pickle', 'rb'))
            time_int: pd.DatetimeIndex = \
                pd.date_range(f'{year}-01-01', periods=periods, freq=freq)

            t_idx: int
            t_idx_str: str
            for t_idx in range(1, periods):
                corr = fx_returns[time_int[t_idx - 1]: time_int[t_idx]].corr()

                if t_idx < 10:
                    t_idx_str = f'0{t_idx}'
                else:
                    t_idx_str = f'{t_idx}'

                hist_data_tools_matrices_physical \
                    .hist_save_data(corr, year, interval, t_idx_str)

            corr = fx_returns[time_int[-1]:].corr()

            if t_idx < 10:
                t_idx_str = f'0{t_idx + 1}'
            else:
                t_idx_str = f'{t_idx + 1}'

            hist_data_tools_matrices_physical \
                .hist_save_data(corr, year, interval, t_idx_str)

        del fx_corr

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

    hist_fx_eigenvectors_physical_data('2019', 'year')

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
