# -*- coding: utf-8 -*-
"""Functions for downloading and analysing data on MPs."""

# Imports ---------------------------------------------------------------------

import numpy as np
import pandas as pd

from . import combine
from . import constants
from . import core
from . import elections
from . import filter
from . import members
from . import utils

# Raw MPs queries -------------------------------------------------------------

def fetch_mps_raw():
    """Fetch key details for all MPs."""
    return members.fetch_members_raw(
        house=constants.PDP_ID_HOUSE_OF_COMMONS)


def fetch_commons_memberships_raw():

    """Fetch Commons memberships for all MPs."""

    commons_memberships_query = """
        PREFIX : <https://id.parliament.uk/schema/>
        PREFIX d: <https://id.parliament.uk/>
        SELECT DISTINCT

            ?person_id
            ?mnis_id
            ?given_name
            ?family_name
            ?display_name
            ?constituency_id
            ?constituency_name
            ?constituency_ons_id
            ?seat_incumbency_id
            ?seat_incumbency_start_date
            ?seat_incumbency_end_date

        WHERE {{

            # House constraint for the House of Commons
            BIND(d:{0} AS ?house)

            ?person_id :memberMnisId ?mnis_id;
                :personGivenName ?given_name ;
                :personFamilyName ?family_name ;
                <http://example.com/F31CBD81AD8343898B49DC65743F0BDF> ?display_name ;
                :memberHasParliamentaryIncumbency ?seat_incumbency_id .
            ?seat_incumbency_id a :SeatIncumbency ;
                :seatIncumbencyHasHouseSeat ?seat ;
                :parliamentaryIncumbencyStartDate ?seat_incumbency_start_date .
            OPTIONAL {{ ?seat_incumbency_id :parliamentaryIncumbencyEndDate ?seat_incumbency_end_date . }}
            ?seat :houseSeatHasHouse ?house ;
                :houseSeatHasConstituencyGroup ?constituency_id .
            ?constituency_id :constituencyGroupName ?constituency_name ;
                :constituencyGroupStartDate ?constituencyStartDate .
            OPTIONAL {{ ?constituency_id :constituencyGroupOnsCode ?constituency_ons_id . }}
        }}
    """.format(constants.PDP_ID_HOUSE_OF_COMMONS)

    return core.sparql_select(commons_memberships_query)


def fetch_mps_party_memberships_raw():
    """Fetch party memberships for all MPs."""
    return members.fetch_party_memberships_raw(
        house=constants.PDP_ID_HOUSE_OF_COMMONS)


def fetch_mps_government_roles_raw():
    """Fetch government roles for all MPs."""
    return members.fetch_government_roles_raw(
        house=constants.PDP_ID_HOUSE_OF_COMMONS)


def fetch_mps_opposition_roles_raw():
    """Fetch opposition roles for all MPs."""
    return members.fetch_opposition_roles_raw(
        house=constants.PDP_ID_HOUSE_OF_COMMONS)


def fetch_mps_committee_memberships_raw():
    """Fetch committee memberships for all MPs."""
    return members.fetch_committee_memberships_raw(
        house=constants.PDP_ID_HOUSE_OF_COMMONS)

# Main MPs API ----------------------------------------------------------------

def fetch_mps(from_date=np.NaN,
              to_date=np.NaN,
              on_date=np.NaN):

    """Fetch key details for all MPs.

    fetch_mps fetches data from the data platform showing key details about
    each MP, with one row per MP.

    The from_date and to_date arguments can be used to filter the MPs returned
    based on the dates of their Commons memberships. The on_date argument is a
    convenience that sets the from_date and to_date to the same given date. The
    on_date has priority: if the on_date is set, the from_date and to_date are
    ignored.

    The filtering is inclusive: an MP is returned if any part of one of their
    Commons memberships falls within the period specified with the from and to
    dates.

    Parameters
    ----------

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
    on_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the on_date.

    Returns
    -------
    out : DataFrame
        A pandas dataframe of key details for each MP, with one row per MP.

    """

    # Set from_date and to_date to on_date if set
    if not pd.isna(on_date):
        from_date = on_date
        to_date = on_date

    # Fetch key details
    mps = fetch_mps_raw()

    # Filter based on membership dates if requested
    if not pd.isna(from_date) or not pd.isna(to_date):
        commons_memberships = fetch_commons_memberships()
        matching_memberships = filter.filter_dates(
            commons_memberships,
            start_col='seat_incumbency_start_date',
            end_col='seat_incumbency_end_date',
            from_date=from_date,
            to_date=to_date)
        mps = mps[mps['person_id'].isin(matching_memberships['person_id'])]

    # Tidy up and return
    mps.sort_values(
        by=['family_name'],
        inplace=True)
    mps.reset_index(drop=True, inplace=True)
    return mps


def fetch_commons_memberships(from_date=np.NaN,
                              to_date=np.NaN,
                              on_date=np.NaN):

    """Fetch Commons memberships for all MPs.

    fetch_commons_memberships fetches data from the data platform showing
    Commons memberships for each MP. The memberships are processed to impose
    consistent rules on the start and end dates for memberships.

    The from_date and to_date arguments can be used to filter the memberships
    returned. The on_date argument is a convenience that sets the from_date and
    to_date to the same given date. The on_date has priority: if the on_date is
    set, the from_date and to_date are ignored.

    The filtering is inclusive: a membership is returned if any part
    of it falls within the period specified with the from and to dates.

    Note that a membership with a NaN end date is still open.

    Parameters
    ----------

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
    on_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the on_date.

    Returns
    -------
    out : DataFrame
        A pandas dataframe of Commons memberships for each MP, with one row
        per Commons membership.

    """

    # Set from_date and to_date to on_date if set
    if not pd.isna(on_date):
        from_date = on_date
        to_date = on_date

    # Fetch the Commons memberships
    commons_memberships = fetch_commons_memberships_raw()

    # Filter on dates if requested
    if not pd.isna(from_date) or not pd.isna(to_date):
        commons_memberships = filter.filter_dates(
            commons_memberships,
            start_col='seat_incumbency_start_date',
            end_col='seat_incumbency_end_date',
            from_date=from_date,
            to_date=to_date)

    # Get elections and fix the end dates of memberships
    end_dates = commons_memberships['seat_incumbency_end_date'].values

    general_elections = elections.get_general_elections().values
    general_elections_count = len(general_elections)

    # If the end date for a membership falls after dissolution adjust it
    for i in range(len(end_dates)):

        date = end_dates[i]
        if pd.isna(date): continue

        for j in range(general_elections_count):

            dissolution = general_elections[j, 1]
            election = general_elections[j, 2]

            if date > dissolution and date <= election:
                end_dates[i] = dissolution
                continue

    commons_memberships['seat_incumbency_end_date'] = end_dates

    # Tidy up and return
    commons_memberships.sort_values(
        by=['family_name',
            'seat_incumbency_start_date'],
        inplace=True)
    commons_memberships.reset_index(drop=True, inplace=True)
    return commons_memberships


def fetch_mps_party_memberships(from_date=np.NaN,
                                to_date=np.NaN,
                                on_date=np.NaN,
                                while_mp=True,
                                collapse=False):

    """Fetch party memberships for all MPs.

    fetch_mps_party_memberships fetches data from the data platform showing
    party memberships for each MP.

    The from_date and to_date arguments can be used to filter the memberships
    returned. The on_date argument is a convenience that sets the from_date and
    to_date to the same given date. The on_date has priority: if the on_date is
    set, the from_date and to_date are ignored.

    The while_mp argument can be used to filter the memberships to include only
    those that occurred during the period when each individual was an MP.

    The filtering is inclusive: a membership is returned if any part
    of it falls within the period specified with the from and to dates.

    The collapse argument controls whether memberships are combined so that
    there is only one row for each period of continuous membership within the
    same party. Combining the memberships in this way means that party
    membership ids from the data platform are not included in the dataframe
    returned.

    Note that a membership with a NaN end date is still open.

    Parameters
    ----------

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
    on_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the on_date.
    while_mp : bool, optional
        A boolean indicating whether to filter the party memberships to include
        only those memberships that were held while each individual was serving
        as an MP. The default value is True.
    collapse: bool, optional
        Determines whether to collapse consecutive memberships within the same
        party into a single period of continuous party membership. Setting this
        to True means that party membership ids are not returned in the
        dataframe. The default value is False.

    Returns
    -------
    out : DataFrame
        A pandas dataframe of party memberships for each MP, with one row per
        party membership. The memberships are processed and merged so that
        there is only one party membership for a period of continuous
        membership within the same party. A membership with a NaN end date is
        still open.

    """

    # Set from_date and to_date to on_date if set
    if not pd.isna(on_date):
        from_date = on_date
        to_date = on_date

    # Fetch the party memberships
    party_memberships = fetch_mps_party_memberships_raw()

    # Filter on dates if requested
    if not pd.isna(from_date) or not pd.isna(to_date):
        party_memberships = filter.filter_dates(
            party_memberships,
            start_col='party_membership_start_date',
            end_col='party_membership_end_date',
            from_date=from_date,
            to_date=to_date)

    # Filter on Commons memberships if requested
    if while_mp:
        commons_memberships = fetch_commons_memberships()
        party_memberships = filter.filter_memberships(
            tm=party_memberships,
            fm=commons_memberships,
            tm_id_col='party_membership_id',
            tm_start_col='party_membership_start_date',
            tm_end_col='party_membership_end_date',
            fm_start_col='seat_incumbency_start_date',
            fm_end_col='seat_incumbency_end_date',
            join_col='person_id')

    # Collapse consecutive memberships and return if requested
    if collapse:
        return combine.combine_party_memberships(party_memberships)

    # Otherwise tidy up and return
    party_memberships.sort_values(
        by=['family_name',
            'party_membership_start_date'],
        inplace=True)
    party_memberships.reset_index(drop=True, inplace=True)

    return party_memberships


def fetch_mps_government_roles(from_date=np.NaN,
                               to_date=np.NaN,
                               on_date=np.NaN,
                               while_mp=True):

    """Fetch government roles for all MPs.

    fetch_mps_government_roles fetches data from the data platform showing
    government roles for each MP.

    The from_date and to_date arguments can be used to filter the roles
    returned. The on_date argument is a convenience that sets the from_date and
    to_date to the same given date. The on_date has priority: if the on_date is
    set, the from_date and to_date are ignored.

    The while_mp argument can be used to filter the roles to include only those
    that occurred during the period when each individual was an MP.

    The filtering is inclusive: a role is returned if any part of it falls
    within the period specified with the from and to dates.

    Note that a role with a NaN end date is still open.

    Parameters
    ----------

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
    on_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the on_date.
    while_mp : bool, optional
        A boolean indicating whether to filter the government roles to include
        only those roles that were held while each individual was serving as an
        MP. The default value is True.

    Returns
    -------
    out : DataFrame
        A dataframe of government roles for each MP, with one row per role.

    """

    # Set from_date and to_date to on_date if set
    if not pd.isna(on_date):
        from_date = on_date
        to_date = on_date

    # Fetch the government roles
    government_roles = fetch_mps_government_roles_raw()

    # Filter on dates if requested
    if not pd.isna(from_date) or not pd.isna(to_date):
        government_roles = filter.filter_dates(
            government_roles,
            start_col='government_incumbency_start_date',
            end_col='government_incumbency_end_date',
            from_date=from_date,
            to_date=to_date)

    # Filter on Commons memberships if requested
    if while_mp:
        commons_memberships = fetch_commons_memberships()
        government_roles = filter.filter_memberships(
            tm=government_roles,
            fm=commons_memberships,
            tm_id_col='government_incumbency_id',
            tm_start_col='government_incumbency_start_date',
            tm_end_col='government_incumbency_end_date',
            fm_start_col='seat_incumbency_start_date',
            fm_end_col='seat_incumbency_end_date',
            join_col='person_id')

    # Tidy up and return
    government_roles.sort_values(
        by=['family_name',
            'government_incumbency_start_date'],
        inplace=True)
    government_roles.reset_index(drop=True, inplace=True)
    return government_roles


def fetch_mps_opposition_roles(from_date=np.NaN,
                               to_date=np.NaN,
                               on_date=np.NaN,
                               while_mp=True):

    """Fetch opposition roles for all MPs.

    fetch_mps_opposition_roles fetches data from the data platform showing
    opposition roles for each MP.

    The from_date and to_date arguments can be used to filter the roles
    returned. The on_date argument is a convenience that sets the from_date and
    to_date to the same given date. The on_date has priority: if the on_date is
    set, the from_date and to_date are ignored.

    The while_mp argument can be used to filter the roles to include only those
    that occurred during the period when each individual was an MP.

    The filtering is inclusive: a role is returned if any part of it falls
    within the period specified with the from and to dates.

    Note that a role with a NaN end date is still open.

    Parameters
    ----------

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
    on_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the on_date.
    while_mp : bool, optional
        A boolean indicating whether to filter the opposition roles to include
        only those roles that were held while each individual was serving as an
        MP. The default value is True.

    Returns
    -------
    out : DataFrame
        A dataframe of opposition roles for each MP, with one row per role.

    """

    # Set from_date and to_date to on_date if set
    if not pd.isna(on_date):
        from_date = on_date
        to_date = on_date

    # Fetch the opposition roles
    opposition_roles = fetch_mps_opposition_roles_raw()

    # Filter on dates if requested
    if not pd.isna(from_date) or not pd.isna(to_date):
        opposition_roles = filter.filter_dates(
            opposition_roles,
            start_col='opposition_incumbency_start_date',
            end_col='opposition_incumbency_end_date',
            from_date=from_date,
            to_date=to_date)

    # Filter on Commons memberships if requested
    if while_mp:
        commons_memberships = fetch_commons_memberships()
        opposition_roles = filter.filter_memberships(
            tm=opposition_roles,
            fm=commons_memberships,
            tm_id_col='opposition_incumbency_id',
            tm_start_col='opposition_incumbency_start_date',
            tm_end_col='opposition_incumbency_end_date',
            fm_start_col='seat_incumbency_start_date',
            fm_end_col='seat_incumbency_end_date',
            join_col='person_id')

    # Tidy up and return
    opposition_roles.sort_values(
        by=['family_name',
            'opposition_incumbency_start_date'],
        inplace=True)
    opposition_roles.reset_index(drop=True, inplace=True)
    return opposition_roles


def fetch_mps_committee_memberships(from_date=np.NaN,
                                    to_date=np.NaN,
                                    on_date=np.NaN,
                                    while_mp=True):

    """Fetch committee memberships for all MPs.

    fetch_mps_commitee_memberships fetches data from the data platform showing
    Parliamentary committee memberships for each MP.

    The from_date, to_date arguments can be used to filter the memberships
    returned based on the given dates. The on_date argument is a convenience
    that sets the from_date and to_date to the same given date. The on_date has
    priority: if the on_date is set, the from_date and to_date are ignored.

    The while_mp argument can be used to filter the memberships to include only
    those that occurred during the period when each individual was an MP.

    The filtering is inclusive: a membership is returned if any part of it
    falls within the period specified with the from and to dates.

    Note that a membership with a NaN end date is still open.

    Parameters
    ----------

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
    on_date : str or date or NaN, optional
        A string or datetime.date representing a date. If a string is used it
        should specify the date in ISO 8601 date format e.g. '2000-12-31'. The
        default value is np.NaN, which means no records are excluded on the
        basis of the on_date.
    while_mp : bool, optional
        A boolean indicating whether to filter the committee memberships to
        include only those memberships that were held while each individual was
        serving as an MP. The default value is True.

    Returns
    -------
    out : DataFrame
        A dataframe of committee memberships for each MP, with one row per
        membership.

    """

    # Set from_date and to_date to on_date if set
    if not pd.isna(on_date):
        from_date = on_date
        to_date = on_date

    # Fetch the committee memberships
    committee_memberships = fetch_mps_committee_memberships_raw()

    # Filter on dates if requested
    if not pd.isna(from_date) or not pd.isna(to_date):
        committee_memberships = filter.filter_dates(
            committee_memberships,
            start_col='committee_membership_start_date',
            end_col='committee_membership_end_date',
            from_date=from_date,
            to_date=to_date)

    # Filter on Commons memberships if requested
    if while_mp:
        commons_memberships = fetch_commons_memberships()
        committee_memberships = filter.filter_memberships(
            tm=committee_memberships,
            fm=commons_memberships,
            tm_id_col='committee_membership_id',
            tm_start_col='committee_membership_start_date',
            tm_end_col='committee_membership_end_date',
            fm_start_col='seat_incumbency_start_date',
            fm_end_col='seat_incumbency_end_date',
            join_col='person_id')

    # Tidy up and return
    committee_memberships.sort_values(
        by=['family_name',
            'committee_membership_start_date'],
        inplace=True)
    committee_memberships.reset_index(drop=True, inplace=True)
    return committee_memberships
