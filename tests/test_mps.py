# -*- coding: utf-8 -*-
"""Test MPs functions."""

# Imports ---------------------------------------------------------------------

import unittest
from unittest.mock import patch

import pdpy.mps as mps
import tests.validate as validate

# Mocks -----------------------------------------------------------------------

def mock_fetch_mps_raw():
    return validate.read('mps_raw')

def mock_fetch_commons_memberships_raw():
    return validate.read('commons_memberships_raw')

def mock_fetch_mps_party_memberships_raw():
    return validate.read('mps_party_memberships_raw')

def mock_fetch_mps_government_roles_raw():
    return validate.read('mps_government_roles_raw')

def mock_fetch_mps_opposition_roles_raw():
    return validate.read('mps_opposition_roles_raw')

def mock_fetch_mps_committee_memberships_raw():
    return validate.read('mps_committee_memberships_raw')

# Tests -----------------------------------------------------------------------

class TestFetchMps(unittest.TestCase):

    """Test fetch_mps processes results correctly."""

    @patch('pdpy.mps.fetch_mps_raw', mock_fetch_mps_raw)
    @patch('pdpy.mps.fetch_commons_memberships_raw',
        mock_fetch_commons_memberships_raw)

    def test_fetch_mps(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'full_title',
            'gender']

        obs = mps.fetch_mps()
        exp = validate.read('fetch_mps')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps(from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_mps_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps(on_date='2017-06-08')
        exp = validate.read('fetch_mps_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchCommonsMemberships(unittest.TestCase):

    """Test fetch_commons_memberships processes results correctly."""

    @patch('pdpy.mps.fetch_commons_memberships_raw',
        mock_fetch_commons_memberships_raw)

    def test_fetch_commons_memberships(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'constituency_id',
            'constituency_name',
            'seat_incumbency_id',
            'seat_incumbency_start_date']

        obs = mps.fetch_commons_memberships()
        exp = validate.read('fetch_commons_memberships')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_commons_memberships(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_commons_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_commons_memberships(on_date='2017-06-08')
        exp = validate.read('fetch_commons_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchMpsPartyMemberships(unittest.TestCase):

    """
    Test fetch_mps_party_memberships processes results correctly.

    """

    @patch('pdpy.mps.fetch_mps_party_memberships_raw',
        mock_fetch_mps_party_memberships_raw)

    def test_fetch_mps_party_memberships(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'party_id',
            'party_mnis_id',
            'party_name',
            'party_membership_start_date']

        obs = mps.fetch_mps_party_memberships()
        exp = validate.read('fetch_mps_party_memberships')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_party_memberships(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_mps_party_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_party_memberships(on_date='2017-06-08')
        exp = validate.read('fetch_mps_party_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_party_memberships(while_mp=False)
        exp = validate.read('fetch_mps_party_memberships_while_mp')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_party_memberships(collapse=True)
        exp = validate.read('fetch_mps_party_memberships_collapse')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchMpsGovernmentRoles(unittest.TestCase):

    """Test fetch_mps_government_roles processes results correctly."""

    @patch('pdpy.mps.fetch_mps_government_roles_raw',
        mock_fetch_mps_government_roles_raw)

    def test_fetch_mps_government_roles(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'position_id',
            'position_name',
            'government_incumbency_id',
            'government_incumbency_start_date']

        obs = mps.fetch_mps_government_roles()
        exp = validate.read('fetch_mps_government_roles')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_government_roles(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_mps_government_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_government_roles(on_date='2017-06-08')
        exp = validate.read('fetch_mps_government_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_government_roles(while_mp=False)
        exp = validate.read('fetch_mps_government_roles_while_mp')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchMpsOppositionRoles(unittest.TestCase):

    """Test fetch_mps_opposition_roles processes results correctly."""

    @patch('pdpy.mps.fetch_mps_opposition_roles_raw',
        mock_fetch_mps_opposition_roles_raw)

    def test_fetch_mps_opposition_roles(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'position_id',
            'position_name',
            'opposition_incumbency_id',
            'opposition_incumbency_start_date']

        obs = mps.fetch_mps_opposition_roles()
        exp = validate.read('fetch_mps_opposition_roles')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_opposition_roles(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_mps_opposition_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_opposition_roles(on_date='2017-06-08')
        exp = validate.read('fetch_mps_opposition_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_opposition_roles(while_mp=False)
        exp = validate.read('fetch_mps_opposition_roles_while_mp')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchMpsCommitteeMemberships(unittest.TestCase):

    """Test fetch_mps_committee_memberships processes results correctly."""

    @patch('pdpy.mps.fetch_mps_committee_memberships_raw',
        mock_fetch_mps_committee_memberships_raw)

    def test_fetch_mps_committee_memberships(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'committee_id',
            'committee_name',
            'committee_membership_id',
            'committee_membership_start_date']

        obs = mps.fetch_mps_committee_memberships()
        exp = validate.read('fetch_mps_committee_memberships')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_committee_memberships(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_mps_committee_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_committee_memberships(on_date='2017-06-08')
        exp = validate.read('fetch_mps_committee_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = mps.fetch_mps_committee_memberships(while_mp=False)
        exp = validate.read('fetch_mps_committee_memberships_while_mp')
        validate.compare_obs_exp(self, obs, exp, cols)
