# -*- coding: utf-8 -*-
"""Functions for combining related records in a dataframe."""

# Imports ---------------------------------------------------------------------

import pandas as pd

from . import utils

# Functions -------------------------------------------------------------------

def combine_party_memberships(pm):

    """Combine consecutive records in a dataframe of party memberships.

    combine_party_memberships takes a datatframe of party memberships and
    combines historically consecutive memberships of the same party into a
    single continuous memberships with the start date of thre first membership
    and the end date of the last. Combining the memberships in this way means
    that party membership ids from the data platform are not included in the
    dataframe returned.

    Parameters
    ----------
    pm : DataFrame
        A pandas dataframe containing party memberships as returned by one of
        the fetch party membership functions.

    Returns
    -------
    out : DataFrame
        A pandas dataframe of party memberships, with one row per party
        membership. The memberships are processed and combined so that there is
        only one party membership for a period of continuous membership within
        the same party.

    """

    # Create a copy of pm
    pm = pm.copy()

    # Check the party memberships dataframe has the expected structure
    required_columns = [
        'person_id',
        'mnis_id',
        'given_name',
        'family_name',
        'display_name',
        'party_id',
        'party_mnis_id',
        'party_name',
        'party_membership_id',
        'party_membership_start_date',
        'party_membership_end_date']

    if len(pm.columns) != len(required_columns) or \
            not (pm.columns == required_columns).all():
        raise ValueError('pm does not have the expected columns')

    # Function to identify consecutive memberships of the same party
    def get_map_party_changes():

        previous_per_par_id = ""
        group_id = 0

        def map_party_changes(per_par_id):
            nonlocal previous_per_par_id
            nonlocal group_id
            if per_par_id != previous_per_par_id:
                previous_per_par_id = per_par_id
                group_id = group_id + 1
            return "{0}-{1}".format(per_par_id, group_id)

        return map_party_changes

    # Sort by person id and membership start date
    pm.sort_values(
        by=['person_id',
            'party_membership_start_date'],
        inplace=True)

    # Create unique combination of person_id and party_id
    pm['per_par_id'] = pm.apply(
        lambda x: '{0}-{1}'.format(x['person_id'], x['party_id']), axis=1)

    # Build an id for consecutive memberships of the same party
    pm['per_par_mem_id'] = pm['per_par_id'].map(get_map_party_changes())

    # Group by person, party and consecutive membership, then take the
    # earliest start date and latest end date
    aggregation = {
        'party_membership_start_date': utils.min_date_nan,
        'party_membership_end_date': utils.max_date_nan
    }

    pmg = pm.groupby([
        'person_id',
        'party_id',
        'per_par_mem_id'])

    pms = pmg.agg(aggregation)
    pms.reset_index(inplace=True)

    pm = pms.merge(
        pm[[
            'person_id',
            'party_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'party_mnis_id',
            'party_name']],
        how='left',
        on=['person_id', 'party_id'])

    pm.drop_duplicates(inplace=True)

    pm = pm[[
        'person_id',
        'mnis_id',
        'given_name',
        'family_name',
        'display_name',
        'party_id',
        'party_mnis_id',
        'party_name',
        'party_membership_start_date',
        'party_membership_end_date']]

    pm.sort_values(
        by=['family_name',
            'party_membership_start_date'],
        inplace=True)
    pm.reset_index(drop=True, inplace=True)

    return pm
