# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # QlikSense data extracted for AL6
# 
# Grouped by Calendar Day and shift name
# 
# SHIFT NAMES
# 
# |Abbr.|German|English|Start Time|
# |-----|------|------|------|
# |FRUE|FRUEH|EARLY|06:00|
# |SPAE|SPAETE|LATE|14:00|
# |NACH|NACHT|NIGHT|22:00|
# 
# 
# ```
# OEE -  ( $(vKPI_Useful_Time) ) / ( $(vKPI_Net_Opening_Time) ) 
# Availability -  ( $(vKPI_Operating_Time) ) / ( $(vKPI_Net_Opening_Time) )
# Performance -  ( $(vKPI_Net_Time) ) / ( $(vKPI_Operating_Time) )
# Quality -  ( $(vKPI_Useful_Time) ) / ( $(vKPI_Net_Time) )
# 
# ```
# 

# %%
import pandas as pd
import numpy as np
import os
from glob import iglob
from common_functions import create_df_from_file

from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# my modules
import set_config


# %%
# call set_config
dir_sanofi_share = set_config.ConfigSectionMap("SectionOne")['sanofi']
dir_local = set_config.ConfigSectionMap("SectionOne")['local']


# %%
# function to read in files we need into a generic df

def create_df_from_excel(indir, infolder, filename):
    df = []
    df_created = pd.DataFrame()
    path = os.path.join(indir, infolder, filename)
    df_created = pd.read_excel(path)
    return df_created

def qs_extract_oee():
    # QlikSense OEE Data extract
    folder = 'IP21_data'

    df_qs_oee = create_df_from_excel(dir_sanofi_share, folder, "AL6_OEE.xlsx")
    df_qs_oee['Calendar Day'] = pd.to_datetime(df_qs_oee['Calendar Day'], format='%y-%b-%d')
    df_qs_oee.set_index('Calendar Day', inplace=True)

    # calc our own OEE with Availability x Performance 
    cols = ['OEE %','Availability %','Performance %']
    df_qs_oee[cols] = df_qs_oee[cols].apply(pd.to_numeric, errors='coerce')
    df_qs_oee['AvailxPerf'] = df_qs_oee['Availability %'] * df_qs_oee['Performance %']
    cols.append('AvailxPerf')
    # df_qs_oee[cols] = df_qs_oee[cols].mul(100)

    df_qs_oee['Shift'] = pd.Categorical(df_qs_oee['Shift Long Name'].str[:4])

    df_qs_oee['Quantity (Pack)'] = df_qs_oee['Quantity (Pack)'].apply(pd.to_numeric, errors='coerce')

    df_qs_oee[cols] = round(df_qs_oee[cols],2)
    # df_qs_oee[(df_qs_oee['OEE %'] - df_qs_oee['AvailxPerf'] !=0) & (df_qs_oee['OEE %'].isna() == False) ][cols]

    return df_qs_oee


if __name__ == '__main__':

    # %%
    get_ipython().run_line_magic('matplotlib', 'inline')

    shifts = df_qs_oee['Shift'].unique()

    fig, axs = plt.subplots(len(shifts), 1, figsize=(20, 15))

    colors = ("red", "purple", "blue", "orange")

    # cols = ['OEE %','McL_OEE']
    cols = ['OEE %','Availability %','Performance %','AvailxPerf']

    i=0

    for s in shifts:
        data = df_qs_oee[df_qs_oee.Shift == s]
        # data.set_index('Calendar Day', inplace=True)
        x=0
        for c in cols:

            data[c].plot(ax=axs[i], c=colors[x])
            # data['Quantity (Pack)'].plot(secondary_y=True, ax=axs[i])
            # set the limits
            axs[i].set_ylim(0,1)
            axs[i].grid(True,which="both", linestyle='--')
            axs[i].set_title('% of OEE for {} shift'.format(s))
            axs[i].legend(loc='upper right', bbox_to_anchor=(1.20, 1.0), fancybox=True)
            x+=1

        i+=1

    # %% [markdown]
    # 

