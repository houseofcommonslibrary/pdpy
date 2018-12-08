# -*- coding: utf-8 -*-
"""Filter functions."""

# Imports ---------------------------------------------------------------------

import datetime
import numpy as np
import pandas as pd

from . import errors

# Filter dates ----------------------------------------------------------------

def filter_dates(df,
                 start_col,
                 end_col,
                 from_date=np.NaN,
                 to_date=np.NaN):

    """Filter a dataframe of data based on the given from and to dates.

    filter_dates takes a dataframe which contains data on a time bound
    activity and returns the subset of rows where that activity took place
    within a given period. The dataframe must contain two columns of
    datetime.date objects, which record the start and end dates of an
    activity. The from and to dates provided are used to find all rows where
    some part of the period of activity took place within the period of
    filtering. The filtering process is tmlusive: as long as at least one day
    of activity falls withinthe filtering period, the row is returned.

    Parameters
    ----------
    df : DataFrame
        A pandas dataframe containing data on a time bound activity.
    start_col : str
        The name of the column that contains the start date for the activity.
    end_col : str
        The name of the column that contains the end date for the activity.
    from_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is numpy.NaN, which means no records are excluded on the
        basis of the from_date.
    to_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the to_date.

    Returns
    -------
    out : DataFrame
        A dataframe with the same structure as the input df containing the
        rows that meet the filtering criteria.

    """

    # Check the start and end columns exist
    if start_col not in df.columns:
        raise errors.MissingColumnError(start_col)

    if end_col not in df.columns:
        raise errors.MissingColumnError(end_col)

    # Check the dataframe has rows
    if df.shape[0] == 0:
        return df

    # Check there are dates to filter
    if pd.isna(from_date) and pd.isna(to_date):
        return df

    # Handle from and to dates
    from_date = handle_date(from_date)
    to_date = handle_date(to_date)

    # Check from date is before to date
    if not pd.isna(from_date) and not pd.isna(to_date) and from_date > to_date:
        raise ValueError('to_date is before from_date')

    # Set default values
    from_after_end = False
    to_before_start = False

    # Get matching rows
    if not pd.isna(from_date):
        from_after_end = df[end_col].map(
            lambda d: False if pd.isna(d) else from_date > d)

    if not pd.isna(to_date):
        to_before_start = df[start_col].map(
            lambda d: False if pd.isna(d) else to_date < d)

    return df[~(from_after_end | to_before_start)]


def handle_date(d):

    """ Take a date which may be a string or a date and returns a date.

    Takes a date which may be a datetime.date or an ISO 8601 date string,
    checks it is valid, and returns the date as a datetime.date. NaN values are
    returned unmodified. This function raises a DateFromatError if it is unable
    to handle the date.

    """

    if pd.isna(d):
        return d
    elif type(d) == datetime.date:
        return d
    elif type(d) == str:
        try:
            return datetime.datetime.strptime(d, '%Y-%m-%d').date()
        except ValueError:
            raise errors.DateFormatError(d)
    else:
        raise TypeError(
            '{0} is not a valid datetime.date or date string'.format(d))

# Filter memberships ----------------------------------------------------------

def filter_memberships(tm,
                       fm,
                       tm_id_col,
                       tm_start_col,
                       tm_end_col,
                       fm_start_col,
                       fm_end_col,
                       join_col):

    """Filter a dataframe of memberships to include only the rows whose period
    of membership intersects with those in another dataframe of memberships.

    filter_memberships is a function to find all memberships in one dataframe
    that intersect with those in another data frame for each person, or other
    entity. This function lets you find things like all committee memberships
    for Commons Members during the period they have served as an MP, or all
    government roles held by Members of the House Lords while they have served
    in the Lords.

    Parameters
    ----------
    tm : DataFrame
        A pandas dataframe containing the target memberships. These are the
        memberships to be filtered.
    fm : DataFrame
        A pandas dataframe containing the filter memberships. These are the
        memberships that are used to filter the target memberships.
    tm_id_col : str
        The name of the column in the target memberships that contains the
        target membership id.
    tm_start_col : str
        The name of the column in target memberships that contains the start
        date for the membership.
    tm_end_col : str
        The name of the column in target memberships that contains the end
        date for the membership.
    fm_start_col : str
        The name of the column in filter memberships that contains the start
        date for the membership.
    fm_end_col : str
        The name of the column in filter memberships that contains the end
        date for the membership.
    join_col : str
        The name of the column in both the target and filter memberships that
        contains the id of the entity that is common to both tables. Where the
        entity is a person this will be the person id.

    Returns
    -------
    out : DataFrame
        A dataframe with the same structure as the input tm containing the rows
        that meet the filtering criteria.

    """

    # Check the target memberships dataframe has rows
    if tm.shape[0] == 0:
        return tm

        # Check the columns exist in each dataframe
    if tm_id_col not in tm.columns:
        raise errors.MissingColumnError(tm_id_col)

    if tm_start_col not in tm.columns:
        raise errors.MissingColumnError(tm_start_col)

    if tm_end_col not in tm.columns:
        raise errors.MissingColumnError(tm_end_col)

    if fm_start_col not in fm.columns:
        raise errors.MissingColumnError(fm_start_col)

    if fm_end_col not in fm.columns:
        raise errors.MissingColumnError(fm_end_col)

    if join_col not in fm.columns:
        raise errors.MissingColumnError(join_col)

    # Create abstract copies of tm and fm
    tma = tm[[join_col, tm_id_col, tm_start_col, tm_end_col]]
    tma.columns = ['join_col', 'tm_id_col', 'tm_start_col', 'tm_end_col']

    fma = fm[[join_col, fm_start_col, fm_end_col]]
    fma.columns = ['join_col', 'fm_start_col', 'fm_end_col']

    # Join the target memberships with the filter membership dates on join_col
    tm_fm = tma.merge(
        fma,
        how='left',
        on='join_col')

    # Function to test if a target membership and filter membership intersect
    def in_fm_func(row):

        # Handle dates
        tm_start_date = row['tm_start_col']
        tm_end_date = row['tm_end_col']
        fm_start_date = row['fm_start_col']
        fm_end_date = row['fm_end_col']
        tm_start_after_fm_end = False
        tm_end_before_fm_start = False

        # Get the match status of the rows
        if not pd.isna(tm_start_date):
            tm_start_after_fm_end = False if pd.isna(fm_end_date) \
                else tm_start_date > fm_end_date

        if not pd.isna(tm_end_date):
            tm_end_before_fm_start = False if pd.isna(fm_start_date) \
                else tm_end_date < fm_start_date

        # Return if the memberships instersect
        return not (tm_start_after_fm_end or tm_end_before_fm_start)

    # Apply the function to each combination of target and filter membership
    tm_fm['in_membership'] = tm_fm.apply(in_fm_func, axis=1)

    # Group the target/filter combinations on the id column
    grouped = tm_fm.groupby('tm_id_col')

    # Check if each target membership intersected with any filter memberships
    match_status = grouped[['in_membership']].any()

    # Restore the actual target membership id column name for joining
    match_status.reset_index(inplace=True)
    match_status.columns = [tm_id_col, 'in_membership']

    # Join the match status with the original target memberships data
    tm_fm_status = tm.merge(
        match_status,
        how='left',
        on=tm_id_col)

    # Return the target memberships after filtering
    tmf = tm_fm_status[tm_fm_status['in_membership']]
    tmf.reset_index(drop=True, inplace=True)
    tmf = tmf.drop(columns=['in_membership'])
    return tmf
