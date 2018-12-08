# -*- coding: utf-8 -*-
"""Test Lords functions."""

# Imports ---------------------------------------------------------------------

import unittest
from unittest.mock import patch

import pdpy.lords as lords
import tests.validate as validate


# Mocks -----------------------------------------------------------------------

def mock_fetch_lords_raw():
    return validate.read('lords_raw')

def mock_fetch_lords_memberships_raw():
    return validate.read('lords_memberships_raw')

def mock_fetch_lords_party_memberships_raw():
    return validate.read('lords_party_memberships_raw')

def mock_fetch_lords_government_roles_raw():
    return validate.read('lords_government_roles_raw')

def mock_fetch_lords_opposition_roles_raw():
    return validate.read('lords_opposition_roles_raw')

def mock_fetch_lords_committee_memberships_raw():
    return validate.read('lords_committee_memberships_raw')

# Tests -----------------------------------------------------------------------

class TestFetchLords(unittest.TestCase):

    """Test fetch_lords processes results correctly."""

    @patch('pdpy.lords.fetch_lords_raw', mock_fetch_lords_raw)
    @patch('pdpy.lords.fetch_lords_memberships_raw',
        mock_fetch_lords_memberships_raw)

    def test_fetch_lords(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'full_title',
            'gender']

        obs = lords.fetch_lords()
        exp = validate.read('fetch_lords')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords(from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_lords_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords(on_date='2017-06-08')
        exp = validate.read('fetch_lords_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchCommonsMemberships(unittest.TestCase):

    """Test fetch_lords_memberships processes results correctly."""

    @patch('pdpy.lords.fetch_lords_memberships_raw',
        mock_fetch_lords_memberships_raw)

    def test_fetch_lords_memberships(self):

        cols = [
            'person_id',
            'mnis_id',
            'given_name',
            'family_name',
            'display_name',
            'seat_type_id',
            'seat_type_name',
            'seat_incumbency_id',
            'seat_incumbency_start_date']

        obs = lords.fetch_lords_memberships()
        exp = validate.read('fetch_lords_memberships')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_memberships(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_lords_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_memberships(on_date='2017-06-08')
        exp = validate.read('fetch_lords_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchLordsPartyMemberships(unittest.TestCase):

    """
    Test fetch_lords_party_memberships processes results correctly.

    """

    @patch('pdpy.lords.fetch_lords_party_memberships_raw',
        mock_fetch_lords_party_memberships_raw)

    def test_fetch_lords_party_memberships(self):

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

        obs = lords.fetch_lords_party_memberships()
        exp = validate.read('fetch_lords_party_memberships')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_party_memberships(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_lords_party_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_party_memberships(on_date='2017-06-08')
        exp = validate.read('fetch_lords_party_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_party_memberships(while_lord=False)
        exp = validate.read('fetch_lords_party_memberships_while_lord')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_party_memberships(collapse=True)
        exp = validate.read('fetch_lords_party_memberships_collapse')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchLordsGovernmentRoles(unittest.TestCase):

    """Test fetch_lords_government_roles processes results correctly."""

    @patch('pdpy.lords.fetch_lords_government_roles_raw',
        mock_fetch_lords_government_roles_raw)

    def test_fetch_lords_government_roles(self):

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

        obs = lords.fetch_lords_government_roles()
        exp = validate.read('fetch_lords_government_roles')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_government_roles(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_lords_government_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_government_roles(on_date='2017-06-08')
        exp = validate.read('fetch_lords_government_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_government_roles(while_lord=False)
        exp = validate.read('fetch_lords_government_roles_while_lord')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchLordsOppositionRoles(unittest.TestCase):

    """Test fetch_lords_opposition_roles processes results correctly."""

    @patch('pdpy.lords.fetch_lords_opposition_roles_raw',
        mock_fetch_lords_opposition_roles_raw)

    def test_fetch_lords_opposition_roles(self):

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

        obs = lords.fetch_lords_opposition_roles()
        exp = validate.read('fetch_lords_opposition_roles')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_opposition_roles(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_lords_opposition_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_opposition_roles(on_date='2017-06-08')
        exp = validate.read('fetch_lords_opposition_roles_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_opposition_roles(while_lord=False)
        exp = validate.read('fetch_lords_opposition_roles_while_lord')
        validate.compare_obs_exp(self, obs, exp, cols)


class TestFetchLordsCommitteeMemberships(unittest.TestCase):

    """Test fetch_lords_committee_memberships processes results correctly."""

    @patch('pdpy.lords.fetch_lords_committee_memberships_raw',
        mock_fetch_lords_committee_memberships_raw)

    def test_fetch_lords_committee_memberships(self):

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

        obs = lords.fetch_lords_committee_memberships()
        exp = validate.read('fetch_lords_committee_memberships')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_committee_memberships(
            from_date='2017-06-08', to_date='2017-06-08')
        exp = validate.read('fetch_lords_committee_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_committee_memberships(on_date='2017-06-08')
        exp = validate.read('fetch_lords_committee_memberships_from_to')
        validate.compare_obs_exp(self, obs, exp, cols)

        obs = lords.fetch_lords_committee_memberships(while_lord=False)
        exp = validate.read('fetch_lords_committee_memberships_while_lord')
        validate.compare_obs_exp(self, obs, exp, cols)
