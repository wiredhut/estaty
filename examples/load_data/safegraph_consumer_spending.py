from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from estaty.paths import get_project_path

import warnings
warnings.filterwarnings('ignore')


def visualization_of_loaded_sample():
    """
    Visualization of pre loaded sample
    URL: https://www.safegraph.com/free-data/spend-data-sample
    """
    df = pd.read_excel(Path(get_project_path(), 'examples', 'load_data',
                            'samples', 'safegraph-spend-sample-q3-2022.xlsx'))
    print('Useful columns: [SPEND_DATE_RANGE_START, SPEND_DATE_RANGE_END,'
          'RAW_TOTAL_SPEND, RAW_NUM_TRANSACTIONS, RAW_NUM_CUSTOMERS,'
          'MEDIAN_SPEND_PER_TRANSACTION, MEDIAN_SPEND_PER_CUSTOMER, '
          'SPEND_PER_TRANSACTION_PERCENTILES, SPEND_BY_DAY, '
          'SPEND_PER_TRANSACTION_BY_DAY,'
          'SPEND_BY_DAY_OF_WEEK, DAY_COUNTS, '
          'SPEND_PCT_CHANGE_VS_PREV_MONTH,'
          'SPEND_PCT_CHANGE_VS_PREV_YEAR, '
          'ONLINE_TRANSACTIONS]')

    df = df.groupby('STREET_ADDRESS').agg({'LONGITUDE': 'mean', 'LATITUDE': 'mean',
                                           'MEDIAN_SPEND_PER_TRANSACTION': 'mean'})
    df = df.reset_index()
    df['MEDIAN_SPEND_PER_TRANSACTION'] = df['MEDIAN_SPEND_PER_TRANSACTION'].astype(float)
    df = df.dropna()

    print(df.head(5))

    with sns.axes_style("darkgrid"):
        sns.scatterplot(data=df, x='LONGITUDE', y='LATITUDE',
                        hue='MEDIAN_SPEND_PER_TRANSACTION',
                        palette='Reds')
        plt.show()


if __name__ == '__main__':
    visualization_of_loaded_sample()
