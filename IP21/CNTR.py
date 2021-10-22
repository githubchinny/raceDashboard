# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # COUNTER ANALYSIS
# 
# First we ASSEMBLE it, after that its been LABELED. Then its PACKAGED and these going into a CARTON. At last the Cartons get PALLETIZED   
# It goes from Assembly (Harro Hoefliger) to Labeler (Krones) to Packaging (Schubert Verpacker) to Cartoner (Pester Umverpacker) to Palletizer (Pester)
# 
# 
# |IP_TAG Name   |Machine|German|Description|Alarm File location|
# |--------------|-------|------|-------------|-------------------| 
# |36630901_CNTR_GOOD|Assembly|Montage|pens rejected between Assembly and Labeler|Y:\E00_Solostar\E6_Assembly_Line_6\E63_Montage\CSV|   
# 

# %%
import pandas as pd
import numpy as np
import os
from glob import iglob

from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# my modules
import set_config
from common_functions import create_df_from_file


# %%
# call set_config
dir_sanofi_share = set_config.ConfigSectionMap("SectionOne")['sanofi']
dir_local = set_config.ConfigSectionMap("SectionOne")['local']


# %%


# read IP21 SPEED files for AL6 packaging machines
def CNTR_Files():
    folder = 'IP21_data'

    # these are the files we are interested in
    # tabIP21Data_36640901_CNTRG.csv             525064
    # tabIP21Data_36630901_CNTR_GOOD.csv         397538
    # tabIP21Data_36650901_CNTR_OUTPUT2.csv       86768
    # tabIP21Data_36630901_CNTRB.csv              26006
    # tabIP21Data_36680901_CNTR_GOOD.csv          24526
    # tabIP21Data_36680902_CNTR_GOOD.csv          24246
    # tabIP21Data_36640901_CNTRB.csv               8425
    # tabIP21Data_36650901_CNTR_BAD_FS_F2.csv      4489
    # tabIP21Data_36680901_FAULT.csv               3151
    # tabIP21Data_36680902_FAULT.csv               2946

    # call function with dir, folder, search criteria to find files, name of dataframe to create
    df_CNTR = create_df_from_file(dir_sanofi_share, folder, "_CNTR_GOOD.csv")
    df_CNTR = df_CNTR.append(create_df_from_file(dir_sanofi_share, folder, "_CNTRG.csv"))
    df_CNTR = df_CNTR.append(create_df_from_file(dir_sanofi_share, folder, "_CNTR_OUTPUT2.csv"))
    df_CNTR = df_CNTR.append(create_df_from_file(dir_sanofi_share, folder, "_CNTRB.csv"))
    df_CNTR = df_CNTR.append(create_df_from_file(dir_sanofi_share, folder, "_CNTR_BAD_FS_F2.csv"))
    df_CNTR = df_CNTR.append(create_df_from_file(dir_sanofi_share, folder, "_FAULT.csv"))

    df_CNTR['IP_TREND_TIME'] = pd.to_datetime(df_CNTR['IP_TREND_TIME'], format='%d-%b-%y %H:%M:%S.%f')


    # %%
    df_CNTR['Machine'] = ''
    df_CNTR.loc[df_CNTR['Name'].str.contains('36630901'), 'Machine'] = 'Assembly'
    df_CNTR.loc[df_CNTR['Name'].str.contains('36640901'), 'Machine'] = 'Labeler'
    df_CNTR.loc[df_CNTR['Name'].str.contains('36650901'), 'Machine'] = 'Packaging'
    df_CNTR.loc[df_CNTR['Name'].str.contains('36680901'), 'Machine'] = 'Cartoner'
    df_CNTR.loc[df_CNTR['Name'].str.contains('36680902'), 'Machine'] = 'Palletizer'
    df_CNTR.loc[df_CNTR['Name'].str.contains('36670901'), 'Machine'] = 'Packaging2'

    df_CNTR['Type'] = ''
    df_CNTR.loc[df_CNTR['Name'].str.contains('CNTRG'), 'Type'] = 'Good'
    df_CNTR.loc[df_CNTR['Name'].str.contains('GOOD'), 'Type'] = 'Good'
    df_CNTR.loc[df_CNTR['Name'].str.contains('OUTPUT'), 'Type'] = 'Good'

    df_CNTR.loc[df_CNTR['Name'].str.contains('CNTRB'), 'Type'] = 'Bad'
    df_CNTR.loc[df_CNTR['Name'].str.contains('BAD'), 'Type'] = 'Bad'
    df_CNTR.loc[df_CNTR['Name'].str.contains('FAULT'), 'Type'] = 'Bad'

    df_CNTR.sort_values(by = ['Name','IP_TREND_TIME'], inplace=True)
    df_CNTR['counter_diff'] = df_CNTR.groupby('Name')['IP_TREND_VALUE'].diff()
    df_CNTR['counter_diff'].loc[df_CNTR.IP_TREND_VALUE < 0] = 0
    df_CNTR['counter_diff'].loc[(df_CNTR.counter_diff < 0) & (df_CNTR.IP_TREND_VALUE == 0)] = 0

    df_CNTR.sort_values(['Name','IP_TREND_TIME'], inplace=True)
    df_CNTR['time_diff'] = df_CNTR.groupby('Name')['IP_TREND_TIME'].diff().dt.total_seconds()
    # df_CNTR.set_index('IP_TREND_TIME', inplace=True)

    # df_CNTR['units_per_sec'] = df_CNTR['counter_diff'] / df_CNTR['time_diff'] 

    return df_CNTR


if __name__ == '__main__':

    machines = ['Assembly', 'Labeler', 'Packaging', 'Cartoner', 'Palletizer']

    i=0

    fig, axs = plt.subplots(len(machines)+1, 1, figsize=(15, 15))

    for x in machines:
        name_filter = '_CNTR_GOOD'
        names = df_CNTR_GOOD[(df_CNTR_GOOD.Name.str.contains(name_filter)) & (df_CNTR_GOOD.Machine == x)].Name.unique()
        # only get files with a count
        # names = df_CNTRB['Name'][df_CNTRB.IP_TREND_VALUE > 0].unique()

        for n in names:
            df_CNTR_GOOD['IP_TREND_VALUE'][df_CNTR_GOOD.Name == n].plot(label=n, ax=axs[i], alpha=0.6)
            # plt.yscale('log')
            axs[i].grid(True,which="both", linestyle='--')
            axs[i].set_title('{} machine for {} files'.format(x, name_filter))
            axs[i].legend(loc='upper right', bbox_to_anchor=(1.20, 1.0), fancybox=True)

        i+=1


    # %%
    # group[group.counter_diff > 20000]
    group.loc['2021-08-06 18:00:00':'2021-08-02 20:00:00'].head(75)


    # %%
    freq='D'

    df_CNTR_GOOD.sort_values(['Machine','IP_TREND_TIME'], inplace=True)
    group = df_CNTR_GOOD.groupby(['Machine','Name',pd.Grouper(freq=freq)]).sum().reset_index()


    # %%
    all = df_CNTR_GOOD.append(df_CNTRB)
    group = all.groupby(['Machine','Name',pd.Grouper(freq=freq)]).sum().reset_index()
    pivot = group.pivot(index='IP_TREND_TIME', columns='Name', values='counter_diff')


    # %%
    df['Machine'] = ''
    df.loc[df['Name_x'].str.contains('36630901'), 'Machine'] = 'Assembly'
    df.loc[df['Name_x'].str.contains('36640901'), 'Machine'] = 'Labeler'
    df.loc[df['Name_x'].str.contains('36650901'), 'Machine'] = 'Packaging'
    df.loc[df['Name_x'].str.contains('36680901'), 'Machine'] = 'Cartoner'
    df.loc[df['Name_x'].str.contains('36680902'), 'Machine'] = 'Palletizer'
    df.loc[df['Name_x'].str.contains('36670901'), 'Machine'] = 'Packaging2'


    # %%
    pivot2 = pivot[['36630901_CNTRB','36650901_CNTR_GOOD','36670901_CNTR_GOOD','36680901_CNTR_GOOD','36680902_CNTR_GOOD','36630901_CNTR_GOOD_ZA']]
    pivot2['36670901_CNTR_GOOD'] = pivot2['36670901_CNTR_GOOD'].astype(np.int64)
    pivot2.head(50)


    # %%
    freq='1h'

    machines = ['Assembly', 'Labeler', 'Packaging', 'Cartoner', 'Palletizer']

    fig, axs = plt.subplots(len(machines), 1, figsize=(15, 15))

    i=0

    for n in names:
        pivot2[n].plot(label=n, ax=axs[i], alpha=0.6)
        # plt.yscale('log')
        axs[i].grid(True,which="both", linestyle='--')
        axs[i].set_title('{} machine for {} files'.format(x, n))
        axs[i].legend(loc='upper right', bbox_to_anchor=(1.20, 1.0), fancybox=True)


        i+=1


    # %%
    # read IP21 SPEED files for AL6 packaging machines
    folder = 'IP21_data'

    # call function with dir, folder, search criteria to find files, name of dataframe to create
    # these are the bad pen counts
    df_CNTR_OUTPUT = create_df_from_file(dir_sanofi_share, folder, "36650901_CNTR_OUTPUT")
    df_CNTR_OUTPUT['IP_TREND_TIME'] = pd.to_datetime(df_CNTR_OUTPUT['IP_TREND_TIME'], format='%d-%b-%y %H:%M:%S.%f')
    df_CNTR_OUTPUT.set_index('IP_TREND_TIME', inplace=True)


    # %%
    df_CNTR_OUTPUT.Name.unique()


    # %%
    names = df_CNTR_OUTPUT.Name.unique()

    for n in names:
        df_CNTR_OUTPUT[df_CNTR_OUTPUT.Name == n].plot()


    # %%
    df_1 = df_CNTR_OUTPUT[df_CNTR_OUTPUT.Name.str.contains('OUTPUT1')]
    df_2 = df_CNTR_OUTPUT[df_CNTR_OUTPUT.Name.str.contains('OUTPUT2')]


    # %%
    df_1.rename(columns={'IP_TREND_VALUE':'OUTPUT1'}, inplace=True)
    df_2.rename(columns={'IP_TREND_VALUE':'OUTPUT2'}, inplace=True)


    # %%
    merge = pd.merge(df_1['OUTPUT1'].sort_index(), df_2['OUTPUT2'].sort_index(), left_index=True, right_index=True)


    # %%
    # merge.reset_index(inplace=True)
    merge['div'] = round(merge.OUTPUT2 / merge.OUTPUT1,0)


    # %%
    merge.groupby('div').count()


    # %%
    merge.set_index('IP_TREND_TIME', inplace=True)


    # %%
    print(df_1.shape)
    print(df_2.shape)


    # %%
    merge[['OUTPUT1','OUTPUT2']].plot(figsize=(15,10))


    # %%
    df_1['OUTPUT1'].plot()


    # %%



