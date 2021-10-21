import pandas as pd
import numpy as np
import os
from glob import iglob

from datetime import datetime
import matplotlib.pyplot as plt

# my modules
import set_config

# call set_config
dir_sanofi_share = set_config.ConfigSectionMap("SectionOne")['sanofi']
dir_local = set_config.ConfigSectionMap("SectionOne")['local']

# function to read in files we need into a generic df
def create_df_from_file(indir, infolder, infilesearch):
    folder = infolder
    path = os.path.join(indir, folder)


    df = []
    df_created = pd.DataFrame()

    # do a recursive search for the files now we have multiple dirs
    for filename in iglob(path + '/**/*' + infilesearch + '*', recursive=True):
        df = pd.read_csv(filename)
        df_created = df_created.append(df)

    return df_created


def ORDER_files():
# %%
    folder = 'IP21_data'

    # call function with dir, folder, search criteria to find files, name of dataframe to create
    # these are the bad pen counts
    df_ORDER = create_df_from_file(dir_sanofi_share, folder, "_ORDER")
    df_ORDER['IP_TREND_TIME'] = pd.to_datetime(df_ORDER['IP_TREND_TIME'], format='%d-%b-%y %H:%M:%S.%f')


    # %%
    names = df_ORDER.Name.unique()
    names


    # %%
    df_ORDER.groupby('Name')['IP_TREND_VALUE'].describe()


    # %%
    df_36630901_ORDERNUMBER = df_ORDER[(df_ORDER.Name == '36630901_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)].copy()
    df_36650901_ORDERNUMBER = df_ORDER[(df_ORDER.Name == '36650901_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)].copy()
    df_36630901_ZA_ORDERNUMBER = df_ORDER[(df_ORDER.Name == '36630901_ZA_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)].copy()

    df_36630901_ORDERNUMBER.rename(columns={'IP_TREND_VALUE':'36630901_ORDERNUMBER'}, inplace=True)
    df_36650901_ORDERNUMBER.rename(columns={'IP_TREND_VALUE':'36650901_ORDERNUMBER'}, inplace=True)
    df_36630901_ZA_ORDERNUMBER.rename(columns={'IP_TREND_VALUE':'36630901_ZA_ORDERNUMBER'}, inplace=True)

    merge = pd.merge(df_36630901_ORDERNUMBER[['IP_TREND_TIME','36630901_ORDERNUMBER']], df_36630901_ZA_ORDERNUMBER[['IP_TREND_TIME','36630901_ZA_ORDERNUMBER']], on='IP_TREND_TIME')
    merge2 = pd.merge(merge, df_36650901_ORDERNUMBER[['IP_TREND_TIME','36650901_ORDERNUMBER']], on='IP_TREND_TIME', how='outer')
    merge3 = pd.DataFrame({'start':merge2.index.iloc[::2].values, 'end':merge2.index.iloc[1::2].values, 'time_diff_mins':merge2.time_diff_mins.iloc[1::2].values})
    for i, row in merge3.iterrows():
        print (i, row[0], row[1])

    # %%
    merge2.sort_values('IP_TREND_TIME', inplace=True)
    return merge2


if __name__ == '__main__':

    # %%
    df_ORDER.sort_values(['Name','IP_TREND_TIME'], inplace=True)
    df_ORDER[(df_ORDER.Name == '36630901_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)]


    # %%
    df_ORDER[(df_ORDER.Name == '36630901_ZA_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)]


    # %%



