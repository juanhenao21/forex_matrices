'''HIST data tools module.

The functions in the module do small repetitive tasks, that are used along the
whole implementation. These tools improve the way the tasks are standardized
in the modules that use them.

This script requires the following modules:
    * matplotlib
    * os
    * pandas
    * pickle

The module contains the following functions:
    * hist_save_data - saves computed data.
    * hist_save_plot - saves figures.
    * hist_function_header_print_data - prints info about the function running.
    * hist_function_header_print_plot - prints info about the plot.
    * hist_start_folders - creates folders to save data and plots.
    * hist_initial_message - prints the initial message with basic information.
    * hist_weeks - generates a tuple with the number of weeks in a year.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

import os
import pickle
from typing import Any, List, Tuple

from matplotlib import pyplot as plt  # type: ignore

# -----------------------------------------------------------------------------


def hist_save_data(data: Any, fx_pair: str, year: str, week: str) -> None:
    """Saves computed data in pickle files.

    Saves the data generated in the functions of the
    hist_data_analysis_extraction module in pickle files.

    :param data: data to be saved. The data can be of different types.
    :param fx_pair: string of the abbreviation of the forex pair to be analyzed
     (i.e. 'eur_usd').
    :param year: string of the year to be analyzed (i.e '2016').
    :param week: string of the week to be analyzed (i.e '07').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    # Saving data

    if (not os.path.isdir(
            f'../../hist_data/physical_basic_data_{year}/hist_fx_physical'
            + f'_basic_data/{fx_pair}/')):

        try:
            os.mkdir(
                f'../../hist_data/physical_basic_data_{year}/hist_fx_physical'
                + f'_basic_data/{fx_pair}/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    pickle.dump(data,
                open(f'../../hist_data/physical_basic_data_{year}/hist_fx'
                     + f'_physical_basic_data/{fx_pair}/hist_fx_physical_basic'
                     + f'_data_{fx_pair}_w{week}.pickle', 'wb'))

    print('Data Saved')
    print()

# -----------------------------------------------------------------------------


def hist_save_plot(function_name: str, figure: plt.Figure, fx_pair: str,
                   year: str, month: str) -> None:
    """Saves plot in png files.

    Saves the plot generated in the functions of the
    hist_data_plot_data_extraction module in png files.

    :param function_name: name of the function that generates the plot.
    :param figure: figure object that is going to be save.
    :param fx_pair: string of the abbreviation of the forex pair to be analyzed
     (i.e. 'eur_usd').
    :param year: string of the year to be analyzed (i.e '2016').
    :param month: string of the month to be analyzed (i.e '07').
    :return: None -- The function save the plot in a file and does not return
     a value.
    """

    # Saving plot data

    if (not os.path.isdir(
            f'../../hist_plot/physical_basic_plot_{year}/{function_name}/')):

        try:
            os.mkdir(f'../../hist_plot/physical_basic_plot_{year}/'
                     + f'{function_name}/')
            print('Folder to save data created')

        except FileExistsError:
            print('Folder exists. The folder was not created')

    figure.savefig(f'../../hist_plot/physical_basic_plot_{year}'
                   + f'/{function_name}/{function_name}_{year}{month}'
                   + f'_{fx_pair}.png')

    print('Plot saved')
    print()

# -----------------------------------------------------------------------------


def hist_function_header_print_data(function_name: str, fx_pair: str,
                                    year: str, week: str) -> None:
    """Prints a header of a function that generates data when it is running.

    :param function_name: name of the function that generates the data.
    :param fx_pair: string of the abbreviation of the forex pair to be analyzed
     (i.e. 'eur_usd').
    :param year: string of the year to be analyzed (i.e '2016').
    :param week: string of the week to be analyzed (i.e '07').
    :return: None -- The function prints a message and does not return a
     value.
    """

    print('HIST data')
    print(function_name)

    fx_pair_upper: str = fx_pair[:3].upper() + '/' + fx_pair[4:].upper()
    print(f'Processing data for the forex pair {fx_pair_upper} in the week '
          + f'{week} of {year}')
    print()

# -----------------------------------------------------------------------------


def hist_function_header_print_plot(function_name: str, fx_pair: str,
                                    year: str, month: str) -> None:
    """Prints a header of a function that generates a plot when it is running.

    :param function_name: name of the function that generates the plot.
    :param fx_pair: string of the abbreviation of the forex pair to be analyzed
     (i.e. 'eur_usd').
    :param year: string of the year to be analyzed (i.e '2016').
    :param month: string of the month to be analyzed (i.e '07').
    :return: None -- The function prints a message and does not return a
     value.
    """

    print('HIST data')
    print(function_name)

    fx_pair_upper: str = fx_pair[:3].upper() + '/' + fx_pair[4:].upper()
    print(f'Processing plot for the forex pair {fx_pair_upper} the '
          + f'{year}.{month}')
    print()

# -----------------------------------------------------------------------------


def hist_start_folders(years: List[str]) -> None:
    """Creates the initial folders to save the data and plots.

    :param year: string of the year to be analyzed (i.e '2016').
    :return: None -- The function creates folders and does not return a value.
    """

    year: str
    for year in years:

        try:
            os.mkdir(f'../../hist_data/physical_basic_data_{year}')
            os.mkdir(f'../../hist_data/physical_basic_data_{year}/hist_fx'
                     + f'_physical_basic_data')
            os.mkdir(f'../../hist_plot/physical_basic_plot_{year}')
            print('Folder to save data created')

        except FileExistsError as error:
            print('Folder exists. The folder was not created')
            print(error)

# -----------------------------------------------------------------------------


def hist_initial_message() -> None:
    """Prints the initial message with basic information.

    :return: None -- The function prints a message and does not return a value.
    """

    print()
    print('########################')
    print('HIST Physical Basic Data')
    print('########################')
    print('AG Guhr')
    print('Faculty of Physics')
    print('University of Duisburg-Essen')
    print('Author: Juan Camilo Henao Londono')
    print('More information in:')
    print('* https://juanhenao21.github.io/')
    print('* https://github.com/juanhenao21/forex_matrices')
    # print('* https://forex-response_spread-year.readthedocs.io/en/latest/')
    print()

# -----------------------------------------------------------------------------


def hist_weeks() -> Tuple[str, ...]:
    """Generates a tuple with the numbers from 0 to 53 representing the weeks
       in a year.

    :return: tuple.
    """

    week_num: List[str] = []

    val: int
    for val in range(1, 54):
        if val < 10:
            val_str: str = f'0{val}'
            week_num.append(f'{val_str}')
        else:
            week_num.append(f'{val}')

    return tuple(week_num)

# -----------------------------------------------------------------------------


def main() -> None:
    """The main function of the script.

    The main function is used to test the functions in the script.

    :return: None.
    """

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()
