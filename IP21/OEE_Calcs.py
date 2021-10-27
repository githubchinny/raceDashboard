import pandas as pd
import numpy as np
import os
import datetime

import set_config
import BATCHACTIVE

# call set_config
dir_sanofi_share = set_config.ConfigSectionMap("SectionOne")['sanofi']
dir_local = set_config.ConfigSectionMap("SectionOne")['local']

# read IP21 SPEED files for AL6 packaging machines
folder = 'IP21_data'

Files = []
df = []
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


# set up start and end periods, or default to all the data

# call changeover - calculated from the BATCHACTIVE files
changeover = BATCHACTIVE.changeover()


# get the batch size

# get the counters

