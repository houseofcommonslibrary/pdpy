# -*- coding: utf-8 -*-
"""Package utility functions."""

# Imports ---------------------------------------------------------------------

import datetime
import numpy as np
import pandas as pd
import requests

# API Functions ---------------------------------------------------------------

def check_api():

    """Check if Python can reach the api and return a boolean."""

    api_url = (
        'https://api.parliament.uk/sparql'
        '?query=SELECT+*+WHERE+%7B+%3Fs+%'
        '3Fp+%3Fo+.+%7D+LIMIT+1%0D%0A')

    try:
        response = requests.get(api_url)
        return response.ok
    except:
        return False

# Date handling functions -----------------------------------------------------

def convert_date_series(date_str_series):

    """Convert a series of ISO 8601 date strings to datetime.dates."""

    return [np.NaN if pd.isna(d) \
        else datetime.datetime.strptime(d, '%Y-%m-%d').date() \
        for d in date_str_series]


def min_date_nan(dates):

    """Find the earliest date from a series that may contain NaNs.

    Find the earliest date from a pandas series of datetime.dates that may
    contain NaNs. NaN dates are considered earlier than all others.

    """

    if dates.isna().any():
        return np.NaN
    else:
        return min(dates)


def max_date_nan(dates):

    """Find the latest date from a series that may contain NaNs.

    Find the latest date from a pandas series of datetime.dates that may
    contain NaNs. NaN dates are considered later than all others.

    """

    if dates.isna().any():
        return np.NaN
    else:
        return max(dates)

# Data presentation functions -------------------------------------------------

def readable(df):

    """Take a dataframe and remove all columns that end in the suffix '_id'.

    The intended purpose of this function is to display a dataframe on the
    console showing only the readable columns i.e. not the identifiers.

    Parameters
    ----------
    df : DataFrame
        A pandas dataframe.

    Returns
    -------
    out : DataFrame
        A dataframe with the same structure as the input df with any columns
        ending in the suffix '_id' removed.

    """

    readable_cols = list(filter(lambda c: not c.endswith('_id'), df.columns))
    return df[readable_cols]
