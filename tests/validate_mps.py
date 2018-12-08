# -*- coding: utf-8 -*-
"""Download data for unit testing MPs."""

# Imports ---------------------------------------------------------------------

import time

import pdpy.constants as constants
import pdpy.mps as mps
import tests.validate as validate

# Mocks data ------------------------------------------------------------------

def fetch_mps_mocks_data():

    """Fetch mocks data for unit tests of MPs."""

    # Download MPs
    m = mps.fetch_mps_raw()
    validate.write(m, 'mps_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download Commons memberships
    cm = mps.fetch_commons_memberships_raw()
    validate.write(cm, 'commons_memberships_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download MP party memberships
    m_pm = mps.fetch_mps_party_memberships_raw()
    validate.write(m_pm, 'mps_party_memberships_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download MP government roles
    m_gor = mps.fetch_mps_government_roles_raw()
    validate.write(m_gor, 'mps_government_roles_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download MP opposition roles
    m_opr = mps.fetch_mps_opposition_roles_raw()
    validate.write(m_opr, 'mps_opposition_roles_raw')
    time.sleep(constants.API_PAUSE_TIME)

    # Download MP committee memberships
    m_cmt = mps.fetch_mps_committee_memberships_raw()
    validate.write(m_cmt, 'mps_committee_memberships_raw')
    time.sleep(constants.API_PAUSE_TIME)

# Validation data -------------------------------------------------------------

def fetch_mps_validation_data():

    """Fetch validation data for unit tests of MPs."""

    # Fetch MPs
    m = mps.fetch_mps()
    validate.write(m, 'fetch_mps')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs with from and to dates
    m = mps.fetch_mps(from_date='2017-06-08', to_date='2017-06-08')
    validate.write(m, 'fetch_mps_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Commons memberships
    cm = mps.fetch_commons_memberships()
    validate.write(cm, 'fetch_commons_memberships')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch Commons memberships with from and to dates
    cm = mps.fetch_commons_memberships(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(cm, 'fetch_commons_memberships_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs party memberships
    pm = mps.fetch_mps_party_memberships()
    validate.write(pm, 'fetch_mps_party_memberships')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs party memberships with from and to dates
    pm = mps.fetch_mps_party_memberships(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(pm, 'fetch_mps_party_memberships_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs party memberships with while_mp
    pm = mps.fetch_mps_party_memberships(while_mp=False)
    validate.write(pm, 'fetch_mps_party_memberships_while_mp')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs party memberships with collapse
    pm = mps.fetch_mps_party_memberships(collapse=True)
    validate.write(pm, 'fetch_mps_party_memberships_collapse')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs government roles
    gor = mps.fetch_mps_government_roles()
    validate.write(gor, 'fetch_mps_government_roles')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs government roles with from and to dates
    gor = mps.fetch_mps_government_roles(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(gor, 'fetch_mps_government_roles_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs government roles with while_mp
    gor = mps.fetch_mps_government_roles(while_mp=False)
    validate.write(gor, 'fetch_mps_government_roles_while_mp')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs opposition roles
    opr = mps.fetch_mps_opposition_roles()
    validate.write(opr, 'fetch_mps_opposition_roles')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs opposition roles with from and to dates
    opr = mps.fetch_mps_opposition_roles(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(opr, 'fetch_mps_opposition_roles_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs opposition roles with while_mp
    opr = mps.fetch_mps_opposition_roles(while_mp=False)
    validate.write(opr, 'fetch_mps_opposition_roles_while_mp')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs committee memberships
    cmt = mps.fetch_mps_committee_memberships()
    validate.write(cmt, 'fetch_mps_committee_memberships')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs committee memberships with from and to dates
    cmt = mps.fetch_mps_committee_memberships(
        from_date='2017-06-08', to_date='2017-06-08')
    validate.write(cmt, 'fetch_mps_committee_memberships_from_to')
    time.sleep(constants.API_PAUSE_TIME)

    # Fetch MPs committee memberships with while_mp
    cmt = mps.fetch_mps_committee_memberships(while_mp=False)
    validate.write(cmt, 'fetch_mps_committee_memberships_while_mp')
    time.sleep(constants.API_PAUSE_TIME)

# Fetch all data --------------------------------------------------------------

def fetch_mps_test_data():

    """Fetch mocks and validation data for unit tests of MPs."""
    fetch_mps_mocks_data()
    fetch_mps_validation_data()
