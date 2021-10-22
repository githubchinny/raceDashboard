import pandas as pd
import os
import re
from glob import iglob

from pandas.core.indexes.datetimes import DatetimeIndex

# function to read in files we need into a generic df
def create_df_from_file(indir, infolder, infilesearch):
    folder = infolder
    path = os.path.join(indir, folder)


    df = []
    df_created = pd.DataFrame()

    # do a recursive search for the files now we have multiple dirs
    for filename in iglob(path + '/**/*' + infilesearch + '*', recursive=True):
        if infilesearch in filename:
            df = pd.read_csv(filename)
            df_created = df_created.append(df)

    return df_created


# build a category column from the index of passed dataframe - assumes DatetimeIndex passed
def create_shift_category(passed_df):

    df = []
    df = passed_df
    
    bins = [0,5,13,21,24]


    labels = ['NIGHT','EARLY','LATE','NIGHT']

    df['Shift'] = pd.cut(df.index.hour,bins=bins, include_lowest=True, labels=labels, ordered=False)

    return df