# -*- coding: utf-8 -*-
"""Download data for unit testing Lords."""

# Imports ---------------------------------------------------------------------

import time

import pdpy.constants as constants
import pdpy.lords as lords
import tests.validate as validate

# Mocks data ------------------------------------------------------------------

def fetch_lords_mocks_data():

    """Fetch mocks data for unit tests of Lords."""

    # Download Lords
    l = lords.fetch_lords_raw()
    validate.write(l, 'lords_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download Lords memberships
    l_cm = lords.fetch_lords_memberships_raw()
    validate.write(l_cm, 'lords_memberships_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download Lords party memberships
    l_pm = lords.fetch_lords_party_memberships_raw()
    validate.write(l_pm, 'lords_party_memberships_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download Lords government roles
    l_gor = lords.fetch_lords_government_roles_raw()
    validate.write(l_gor, 'lords_government_roles_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download Lords opposition roles
    l_opr = lords.fetch_lords_opposition_roles_raw()
    validate.write(l_opr, 'lords_opposition_roles_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download Lords committee memberships
    l_ctm = lords.fetch_lords_committee_memberships_raw()
    validate.write(l_ctm, 'lords_committee_memberships_raw')
    time.sleep(constants.API_PAUSE_TIME)

# Validation data -------------------------------------------------------------

def fetch_lords_validation_data():

    """Fetch validation data for unit tests of Lords."""

    # Fetch Lords
    l = lords.fetch_lords()
    validate.write(l, 'fetch_lords')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords with from and to dates
    l = lords.fetch_lords(from_date='2017-06-08', to_date='2017-06-08')
    validate.write(l, 'fetch_lords_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords memberships
    lm = lords.fetch_lords_memberships()
    validate.write(lm, 'fetch_lords_memberships')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords memberships with from and to dates
    lm = lords.fetch_lords_memberships(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(lm, 'fetch_lords_memberships_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords party memberships
    pm = lords.fetch_lords_party_memberships()
    validate.write(pm, 'fetch_lords_party_memberships')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords party memberships with from and to dates
    pm = lords.fetch_lords_party_memberships(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(pm, 'fetch_lords_party_memberships_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords party memberships with while_lord
    pm = lords.fetch_lords_party_memberships(while_lord=False)
    validate.write(pm, 'fetch_lords_party_memberships_while_lord')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords party memberships with collapse
    pm = lords.fetch_lords_party_memberships(collapse=True)
    validate.write(pm, 'fetch_lords_party_memberships_collapse')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords government roles
    gor = lords.fetch_lords_government_roles()
    validate.write(gor, 'fetch_lords_government_roles')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords government roles with from and to dates
    gor = lords.fetch_lords_government_roles(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(gor, 'fetch_lords_government_roles_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords government roles with while_lord
    gor = lords.fetch_lords_government_roles(while_lord=False)
    validate.write(gor, 'fetch_lords_government_roles_while_lord')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords opposition roles
    opr = lords.fetch_lords_opposition_roles()
    validate.write(opr, 'fetch_lords_opposition_roles')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords opposition roles with from and to dates
    opr = lords.fetch_lords_opposition_roles(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(opr, 'fetch_lords_opposition_roles_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords opposition roles with while_lord
    opr = lords.fetch_lords_opposition_roles(while_lord=False)
    validate.write(opr, 'fetch_lords_opposition_roles_while_lord')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords committee memberships
    cmt = lords.fetch_lords_committee_memberships()
    validate.write(cmt, 'fetch_lords_committee_memberships')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords committee memberships with from and to dates
    cmt = lords.fetch_lords_committee_memberships(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(cmt, 'fetch_lords_committee_memberships_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Lords committee memberships with while_lord
    cmt = lords.fetch_lords_committee_memberships(while_lord=False)
    validate.write(cmt, 'fetch_lords_committee_memberships_while_lord')
    time.sleep(constants.API_PAUSE_TIME)

# Fetch all data --------------------------------------------------------------

def fetch_lords_test_data():

    """Fetch mocks and validation data for unit tests of Lords."""
    fetch_lords_mocks_data()
    fetch_lords_validation_data()
