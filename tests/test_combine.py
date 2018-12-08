# -*- coding: utf-8 -*-
"""Test combine functions."""

# Imports ---------------------------------------------------------------------

import datetime
import io
import numpy as np
import pandas as pd
import unittest

import pdpy.combine as combine
import pdpy.errors as errors
import pdpy.utils as utils


# Test data -------------------------------------------------------------------

pm_csv = """
    person_id,  membership_id,  party_id,   start_date, end_date
    p1,         m1,             pa1,        2001-01-01, 2001-12-31
    p1,         m2,             pa2,        2002-01-01, 2002-12-31
    p1,         m3,             pa1,        2003-01-01, 2003-12-31
    p1,         m4,             pa1,        2004-01-01, 2004-12-31
    p2,         m5,             pa1,        2002-01-01, 2002-12-31
    p2,         m6,             pa2,        2004-01-01, NA
    p2,         m7,             pa2,        2003-01-01, 2003-12-31
    p2,         m8,             pa1,        2001-01-01, 2001-12-31
"""

pm = pd.read_csv(io.BytesIO(bytes(pm_csv, encoding='utf-8')),
                 skipinitialspace = True)

pm['party_membership_start_date'] = utils.convert_date_series(pm['start_date'])
pm['party_membership_end_date'] = utils.convert_date_series(pm['end_date'])
pm['mnis_id'] = ''
pm['given_name'] = pm['person_id']
pm['family_name'] = pm['person_id']
pm['display_name'] = pm['person_id']
pm['party_membership_id'] = ''
pm['party_mnis_id'] = ''
pm['party_name'] = ''
pm = pm[[
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
    'party_membership_end_date']]

class CombinePartyMemberships(unittest.TestCase):

    """
    Test that combine_party_memberships returns a DataFrame with the
    expected properties.

    """

    def test_that_combine_party_memberships_raises_value_error(self):

        with self.assertRaises(ValueError):
            pm_missing_column = pm.drop('person_id', axis=1)
            cpm = combine.combine_party_memberships(pm_missing_column)

        with self.assertRaises(ValueError):
            pm_wrong_column_names = pm.drop('person_id', axis=1)
            pm_wrong_column_names['pid'] = pm['person_id']
            cpm = combine.combine_party_memberships(pm_wrong_column_names)

    def test_that_filter_memberships_filters_correct_memberships(self):

        cpm = combine.combine_party_memberships(pm)

        self.assertEqual(cpm.shape[0], 5)
        self.assertEqual(cpm.shape[1], pm.shape[1] - 1)

        expected_columns = pm.drop('party_membership_id', axis=1).columns
        self.assertEqual((cpm.columns == expected_columns).all(), True)

        self.assertEqual((cpm['person_id'] == [
            'p1', 'p1', 'p1', 'p2', 'p2']).all(), True)

        self.assertEqual((cpm['party_membership_start_date'] == [
            datetime.date(2001, 1, 1),
            datetime.date(2002, 1, 1),
            datetime.date(2003, 1, 1),
            datetime.date(2001, 1, 1),
            datetime.date(2003, 1, 1)]).all(), True)

        self.assertEqual((cpm['party_membership_end_date'][0:4] == [
            datetime.date(2001, 12, 31),
            datetime.date(2002, 12, 31),
            datetime.date(2004, 12, 31),
            datetime.date(2002, 12, 31)]).all(), True)

        self.assertTrue(pd.isna(cpm['party_membership_end_date'].iloc[4]))
