import os
import sys
import argparse

import pandas   as pd
import numpy    as np

import matplotlib.pyplot as plt


def specify_types(dataframe):
    dataframe = dataframe.astype({
        'Region':                       'string',
        'PCR tests confirmed (all)':    'float64'
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
            'ELISA tests conducted (s?)', # Сумарні
            'ELISA tests conducted (t?)', # Разом (IgA+IgM+IgG+Сумарні)
            'ELISA tests confirmed (IgA)',
            'ELISA tests confirmed (IgM)',
            'ELISA tests confirmed (IgG)',
            'ELISA tests confirmed (s?)', # Сумарні
            'ELISA tests confirmed (t?)', # Разом (IgA+IgM+IgG+Сумарні)
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
            '(?) ELISA tests conducted (s?)',                     # ?
            '(?) ELISA tests conducted (t?)',                     # ?
            '(?) ELISA tests confirmed (IgA)',                    # ?
            '(?) ELISA tests confirmed (IgM)',                    # ?
            '(?) ELISA tests confirmed (IgG)',                    # ?
            '(?) ELISA tests confirmed (s?)',                     # ?
            '(?) ELISA tests confirmed (t?)',                     # ?
            '(?) ELISA tests confirmed (medics)',                 # ?
            '(?) ELISA tests confirmed (police)'                  # ?
        ],
        usecols     = [
            'Region',
            'PCR tests confirmed (all)'
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

    parser.add_argument('-d', '--data', default = './data/conducted tests/fixed/2020/10', help='Directory with data sets')
    
    options = parser.parse_args(arguments)
    
    return options


def main(arguments):
    options = parse_cli_arguments(arguments)

    datasets_dir = options.data
    
    dataframe       = load_data(datasets_dir)
    dataframe_dp    = dataframe[dataframe.Region.eq('Дніпропетровська')]
    
    dataframe_by_date       = dataframe.groupby(dataframe.index).sum()
    dataframe_db_by_date    = dataframe_dp.groupby(dataframe_dp.index).sum()

    figure, axes = plt.subplots()
    
    axes.plot(dataframe_by_date,    label = 'Total')
    axes.plot(dataframe_db_by_date, label = 'Dnipropetrovsk region')
    
    axes.legend(loc='right')
    axes.grid(True)
    
    axes.set_ylabel('confirmed')
    axes.set_title('PCR tests')
    
    plt.xticks(rotation = 45)
    
    plt.show()




    #print(dataframe)
    #print(dataframe.head())
    #print(dataframe.info())
    #print(dataframe.dtypes)
    #print(type(dataframe))


if __name__ == '__main__':
    # first argument is script name, so we pass all arguments except of scipt name
    sys.exit(main(sys.argv[1:]))