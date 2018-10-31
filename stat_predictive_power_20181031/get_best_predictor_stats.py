#!/usr/bin/env python3
'''
Rank which offensive statistics by how well they correlated with
various stats of interest from 2017 to 2018
'''

import re

from scipy import stats
import pandas as pd

# Contains various per-season stats and limited descriptive info for
# all hitters with at least 200 PAs in either 2017 or 2018.
# Obtained via exporting data from the following URL:
# https://www.fangraphs.com/leaders.aspx?pos=np&stats=bat&lg=all&qual=200&type=c,4,6,11,12,13,21,34,35,41,23,37,38,44,45,43,102,103,104,105,106,107&season=2018&month=0&season1=2017&ind=1&team=0&rost=0&age=0&filter=&players=0&sort=5,a
CSV_FILENAME = 'hitters_2017_2018.csv'


def main():
    '''
    Run the script
    '''
    data_frame = pd.read_csv(CSV_FILENAME)

    # Add HR Rate column
    data_frame['HRRate'] = data_frame['HR'] / data_frame['PA']

    rate_stats = [
        'BB%',
        'K%',
        'AVG',
        'OBP',
        'SLG',
        'GB%',
        'FB%',
        'LD%',
        'O-Swing%',
        'Z-Swing%',
        'Swing%',
        'O-Contact%',
        'Z-Contact%',
        'Contact%',
    ]

    stats_of_interest = [
        'HRRate',
        'OBP',
        'AVG',
        'RBI',  # Predict rate RBI, R, SB rate stats?
        'R',
        'SB',
    ]

    # If the stat's name ends in '%', need to strip any % off back of
    # values and convert to floats
    for rate_stat in rate_stats:
        if rate_stat.endswith('%'):
            data_frame[rate_stat] = data_frame[rate_stat].apply(lambda x: re.sub(r'\s*%$', '', x))
            data_frame[rate_stat] = data_frame[rate_stat].apply(pd.to_numeric)

    for stat_of_interest in stats_of_interest:
        correlations = {}
        for rate_stat in rate_stats:
            if rate_stat == stat_of_interest:
                continue
            pearson_coef, _ = stats.pearsonr(data_frame[rate_stat], data_frame[stat_of_interest])
            correlations[rate_stat] = pearson_coef ** 2

        print('-' * 45)
        print(stat_of_interest)
        print('-' * 45)
        print('{:<20} {:<15}'.format('Target Stat', 'Correlation'))
        for rate_stat in dict(sorted(correlations.items(), key=lambda key_val_pair: key_val_pair[1], reverse=True)):
            print('{xstat:<20} {correlation:<15}'
                  .format(xstat=rate_stat,
                          correlation=correlations[rate_stat]))
        print('')


if __name__ == '__main__':
    main()
