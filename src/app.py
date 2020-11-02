import os
import sys
import argparse

import pandas   as pd
import numpy    as np

import matplotlib.pyplot    as plt
import matplotlib.dates     as mdates


def specify_types(dataframe):
    dataframe = dataframe.astype({
        'Region':                       'string',
        'PCR tests confirmed (all)':    'float64',
        'PCR tests conducted':          'float64'
    })

    return dataframe

def add_date_column(dataframe, dataset_date):
    rows_count          = len(dataframe.index)
    date_column_values  = np.full(rows_count, dataset_date)

    dataframe.insert(0, 'Date', date_column_values)
    dataframe.set_index('Date', inplace=True)

    return dataframe

def load_daily_data(file_path):
    dataframe = pd.read_csv(
        file_path,
        delimiter   = ';',
        names       = [
            'Region',
            'Laboratory',
            'PCR tests conducted',
            'PCR tests conducted of pneumonia patients',
            'PCR tests of pneumonia patients (confirmed)',
            'PCR tests confirmed (all)',
            'PCR tests confirmed (medics)',
            'PCR tests confirmed (police)',
            'PCR tests retesting results (all)',        # retesting is done to check if
            'PCR tests retesting results (confirmed)',  # source about retesting meaning - interview of head of Cented of Public Health https://ua.112.ua/zdorovie/koronavirus-mozhut-diahnostuvaty-patsiientu-z-vazhkym-perebihom-zakhvoriuvannia-popry-nehatyvnyi-test-536397.html
            'PCR Samples leftovers (all)',
            'PCR Samples leftovers (priority 1)',
            'PCR Samples leftovers (priority 2)',
            'PCR Samples leftovers (priority 3)',
            'ELISA tests conducted (IgA)',
            'ELISA tests conducted (IgM)',
            'ELISA tests conducted (IgG)',
            'ELISA tests conducted (Total)',    # total  antibodies test (including IgM, IgA and IgG) (IgA included?)
            'ELISA tests conducted (Sum)',      # sum of all tests (IgM + IgA + IgG + Total)
            'ELISA tests confirmed (IgA)',
            'ELISA tests confirmed (IgM)',
            'ELISA tests confirmed (IgG)',
            'ELISA tests confirmed (Total)',    # total  antibodies test (including IgM, IgA and IgG) (IgA included?)
            'ELISA tests confirmed (Sum)',      # sum of all tests (IgM + IgA + IgG + Total)
            'ELISA tests confirmed (medics)',
            'ELISA tests confirmed (police)',
            'ELISA Samples leftovers',
            '(?) PCR tests conducted',                            # ? for the entire period (period - from pandemic start?)
            '(?) PCR tests conducted of pneumonia patients',      # ?
            '(?) PCR tests of pneumonia patients (confirmed)',    # ?
            '(?) PCR tests confirmed (all)',                      # ?
            '(?) PCR tests confirmed (medics)',                   # ?
            '(?) PCR tests confirmed (police)',                   # ?
            '(?) ELISA tests conducted (IgA)',                    # ?
            '(?) ELISA tests conducted (IgM)',                    # ?
            '(?) ELISA tests conducted (IgG)',                    # ?
            '(?) ELISA tests conducted (Total)',                  # total  antibodies test (including IgM, IgA and IgG) (IgA included?)
            '(?) ELISA tests conducted (Sum)',                    # sum of all tests (IgM + IgA + IgG + Total)
            '(?) ELISA tests confirmed (IgA)',                    # ?
            '(?) ELISA tests confirmed (IgM)',                    # ?
            '(?) ELISA tests confirmed (IgG)',                    # ?
            '(?) ELISA tests confirmed (Total)',                  # total  antibodies test (including IgM, IgA and IgG) (IgA included?)
            '(?) ELISA tests confirmed (Sum)',                    # sum of all tests (IgM + IgA + IgG + Total)
            '(?) ELISA tests confirmed (medics)',                 # ?
            '(?) ELISA tests confirmed (police)'                  # ?
        ],
        usecols     = [
            'Region',
            'PCR tests confirmed (all)',
            'PCR tests conducted'
        ]
    )

    return dataframe

def load_data(datasets_dir):
    if os.path.exists(datasets_dir) == False:
        raise ValueError(f"data sets directory '{datasets_dir}' not found")

    daily_frames = []
    for root, dirs, files in os.walk(datasets_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            dataset_date = os.path.splitext(file_name)[0].replace('tests_', '').replace('_', '.')

            dataframe = load_daily_data(file_path)

            dataframe = add_date_column(dataframe, dataset_date)
            dataframe = specify_types(dataframe)

            daily_frames.append(dataframe)

    merged_daily_frames = pd.concat(daily_frames)

    return merged_daily_frames

def parse_cli_arguments(arguments):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--data',     default = './data/conducted tests/fixed/2020/10',   help='Directory with data sets')
    parser.add_argument('-r', '--region',   default = 'Дніпропетровська',                       help='Name of the region to compare with general data')

    options = parser.parse_args(arguments)

    return options

def draw_plots(dataframe, color, label, axis):
    dataframe.plot(
        y           = 'PCR tests conducted',
        linestyle   = '--',

        label       = f'{label} (conducted)',
        color       = color,
        ax          = axis
    )

    dataframe.plot(
        y           = 'PCR tests confirmed (all)',

        label       = f'{label} (positive)',
        color       = color,
        ax          = axis
    )


def main(arguments):
    options = parse_cli_arguments(arguments)

    datasets_dir    = options.data
    region_name     = options.region

    dataframe           = load_data(datasets_dir)
    dataframe_region    = dataframe[dataframe.Region.eq(region_name)]

    dataframe_by_date           = dataframe.groupby(dataframe.index).sum()
    dataframe_region_by_date    = dataframe_region.groupby(dataframe_region.index).sum()

    figure, axis = plt.subplots()

    draw_plots(
        dataframe   = dataframe_by_date,
        color       = 'red',
        label       = 'Total',
        axis        = axis
    )

    draw_plots(
        dataframe   = dataframe_region_by_date,
        color       = 'blue',
        label       = region_name,
        axis        = axis
    )

    axis.legend(loc='right')
    axis.grid(True)

    axis.set_ylabel('tests count')
    axis.set_title('PCR tests')

    plt.xticks(rotation = 45)
    plt.xticks(range(0, len(dataframe_by_date.index)), dataframe_by_date.index)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    figure.tight_layout()

    plt.show()




    #print(dataframe)
    #print(dataframe.head())
    #print(dataframe.info())
    #print(dataframe.dtypes)
    #print(type(dataframe))


if __name__ == '__main__':
    # first argument is script name, so we pass all arguments except of scipt name
    sys.exit(main(sys.argv[1:]))