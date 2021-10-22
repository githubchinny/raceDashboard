import pandas as pd
import numpy as np
import os
from glob import iglob

from datetime import datetime
import matplotlib.pyplot as plt

# my modules
import set_config
from common_functions import create_df_from_file

# call set_config
dir_sanofi_share = set_config.ConfigSectionMap("SectionOne")['sanofi']
dir_local = set_config.ConfigSectionMap("SectionOne")['local']


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
    # merge3 = pd.DataFrame({'start':merge2.IP_TREND_VALUE.iloc[::2].values, 'end':merge2.IP_TREND_VALUE.iloc[1::2].values, 'time_diff_mins':merge2.time_diff_mins.IP_TREND_VALUE.iloc[1::2].values})

    # %%
    merge2.sort_values('IP_TREND_TIME', inplace=True)

    df_BATCHID = create_df_from_file(dir_sanofi_share, folder, "_BATCHID.csv")
    df_BATCHID['IP_TREND_TIME'] = pd.to_datetime(df_BATCHID['IP_TREND_TIME'], format='%d-%b-%y %H:%M:%S.%f')

    df_MATNO = create_df_from_file(dir_sanofi_share, folder, "_MATNO.csv")
    df_MATNO['IP_TREND_TIME'] = pd.to_datetime(df_MATNO['IP_TREND_TIME'], format='%d-%b-%y %H:%M:%S.%f')

    merge3 = pd.merge(merge2, df_BATCHID[['IP_TREND_TIME','IP_TREND_VALUE']], left_on='IP_TREND_TIME', right_on='IP_TREND_TIME', how='left')
    merge3.rename(columns={'IP_TREND_VALUE':'BATCH_ID'}, inplace=True)

    merge4 = pd.merge(merge3, df_MATNO[['IP_TREND_TIME','IP_TREND_VALUE']], left_on='IP_TREND_TIME', right_on='IP_TREND_TIME', how='left')
    merge4.rename(columns={'IP_TREND_VALUE':'BATCH_SIZE'}, inplace=True)

    return merge4




if __name__ == '__main__':

    # %%
    df_ORDER.sort_values(['Name','IP_TREND_TIME'], inplace=True)
    df_ORDER[(df_ORDER.Name == '36630901_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)]


    # %%
    df_ORDER[(df_ORDER.Name == '36630901_ZA_ORDERNUMBER') & (df_ORDER.IP_TREND_VALUE.isna() == False)]


    # %%



