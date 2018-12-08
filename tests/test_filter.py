# -*- coding: utf-8 -*-
"""Test filter functions."""

# Imports ---------------------------------------------------------------------

import datetime
import io
import numpy as np
import pandas as pd
import unittest

import pdpy.errors as errors
import pdpy.filter as filter
import pdpy.utils as utils


# Test data -------------------------------------------------------------------

mem_a_csv = """
    person_id,  membership_id,  start_date,     end_date
    p1,         a1,             2001-01-01,     2001-12-31
    p1,         a2,             2005-01-01,     2005-12-31
    p1,         a3,             2006-01-01,     2006-12-31
    p1,         a4,             2010-01-01,     2010-12-31
    p2,         a5,             2005-01-01,     2005-12-31
    p2,         a6,             2006-01-01,     2006-12-31
    p2,         a7,             2010-01-01,     2010-12-31
    p2,         a8,             2015-01-01,     2015-12-31
"""

mem_b_csv = """
    person_id,  membership_id,  start_date,     end_date
    p1,         b1,             2001-06-01,     2002-06-30
    p1,         b2,             2004-01-01,     2004-12-31
    p1,         b3,             2006-01-01,     2006-12-31
    p1,         b4,             2011-01-01,     2011-12-31
    p2,         b5,             2004-01-01,     2004-12-31
    p2,         b6,             2006-01-01,     2006-12-31
    p2,         b7,             2011-01-01,     2011-12-31
    p2,         b8,             2015-06-01,     2016-06-30
"""

mem_a = pd.read_csv(
    io.BytesIO(bytes(mem_a_csv, encoding='utf-8')),
    skipinitialspace = True)
mem_a['start_date'] = utils.convert_date_series(mem_a['start_date'])
mem_a['end_date'] = utils.convert_date_series(mem_a['end_date'])

mem_b = pd.read_csv(
    io.BytesIO(bytes(mem_b_csv, encoding='utf-8')),
    skipinitialspace = True)
mem_b['start_date'] = utils.convert_date_series(mem_b['start_date'])
mem_b['end_date'] = utils.convert_date_series(mem_b['end_date'])

# Test filter_dates -----------------------------------------------------------

class TestFilterDates(unittest.TestCase):

    """
    Test that filter_dates returns a DataFrame with the expected properties.

    """

    def test_that_filter_dates_raises_missing_column_error(self):

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_dates(
                mem_a,
                start_col='no_such_column',
                end_col='end_date')

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_dates(
                mem_a,
                start_col='start_date',
                end_col='no_such_column')

    def test_that_filter_dates_raises_value_error(self):

        with self.assertRaises(ValueError):

            f_mem_a = filter.filter_dates(
                mem_a,
                start_col='start_date',
                end_col='end_date',
                from_date='2010-01-01',
                to_date='2009-12-31')

    def test_that_filter_dates_raises_date_format_error(self):

        with self.assertRaises(errors.DateFormatError):

            f_mem_a = filter.filter_dates(
                mem_a,
                start_col='start_date',
                end_col='end_date',
                from_date='2010-01-XX',
                to_date='2010-12-31')

        with self.assertRaises(errors.DateFormatError):

            f_mem_a = filter.filter_dates(
                mem_a,
                start_col='start_date',
                end_col='end_date',
                from_date='2010-01-01',
                to_date='2010-12-XX')

    def test_filter_dates_does_not_filter_without_dates(self):

        f_mem_a = filter.filter_dates(
            mem_a,
            start_col='start_date',
            end_col='end_date')

        self.assertEqual(f_mem_a.shape, mem_a.shape)
        self.assertTrue((f_mem_a == mem_a).all().all())

    def test_filter_dates_excludes_rows_before_from_date(self):

        f_mem_a = filter.filter_dates(
            mem_a,
            start_col='start_date',
            end_col='end_date',
            from_date='2004-12-31')

        self.assertEqual(f_mem_a.shape[0], mem_a.shape[0] - 1)
        self.assertEqual(f_mem_a.shape[1], mem_a.shape[1])

        self.assertEqual(f_mem_a.iloc[0]['person_id'], 'p1')
        self.assertEqual(f_mem_a.iloc[0]['membership_id'], 'a2')
        self.assertEqual(f_mem_a.iloc[0]['start_date'],
            datetime.date(2005, 1, 1))
        self.assertEqual(f_mem_a.iloc[0]['end_date'],
            datetime.date(2005, 12, 31))

    def test_filter_dates_excludes_rows_after_to_date(self):

        f_mem_a = filter.filter_dates(
            mem_a,
            start_col='start_date',
            end_col='end_date',
            to_date='2011-01-01')

        self.assertEqual(f_mem_a.shape[0], mem_a.shape[0] - 1)
        self.assertEqual(f_mem_a.shape[1], mem_a.shape[1])

        self.assertEqual(f_mem_a.iloc[-1]['person_id'], 'p2')
        self.assertEqual(f_mem_a.iloc[-1]['membership_id'], 'a7')
        self.assertEqual(f_mem_a.iloc[-1]['start_date'],
            datetime.date(2010, 1, 1))
        self.assertEqual(f_mem_a.iloc[-1]['end_date'],
            datetime.date(2010, 12, 31))

    def test_filter_dates_excludes_rows_outside_both_dates(self):

        f_mem_a = filter.filter_dates(
            mem_a,
            start_col='start_date',
            end_col='end_date',
            from_date='2004-12-31',
            to_date='2011-01-01')

        self.assertEqual(f_mem_a.shape[0], mem_a.shape[0] - 2)
        self.assertEqual(f_mem_a.shape[1], mem_a.shape[1])

        self.assertEqual(f_mem_a.iloc[0]['person_id'], 'p1')
        self.assertEqual(f_mem_a.iloc[0]['membership_id'], 'a2')
        self.assertEqual(f_mem_a.iloc[0]['start_date'],
            datetime.date(2005, 1, 1))
        self.assertEqual(f_mem_a.iloc[0]['end_date'],
            datetime.date(2005, 12, 31))

        self.assertEqual(f_mem_a.iloc[-1]['person_id'], 'p2')
        self.assertEqual(f_mem_a.iloc[-1]['membership_id'], 'a7')
        self.assertEqual(f_mem_a.iloc[-1]['start_date'],
            datetime.date(2010, 1, 1))
        self.assertEqual(f_mem_a.iloc[-1]['end_date'],
            datetime.date(2010, 12, 31))

    def test_filter_dates_includes_rows_with_partial_instersection(self):

        f_mem_a = filter.filter_dates(
            mem_a,
            start_col='start_date',
            end_col='end_date',
            from_date='2005-06-30',
            to_date='2010-06-30')

        self.assertEqual(f_mem_a.shape[0], mem_a.shape[0] - 2)
        self.assertEqual(f_mem_a.shape[1], mem_a.shape[1])

        self.assertEqual(f_mem_a.iloc[0]['person_id'], 'p1')
        self.assertEqual(f_mem_a.iloc[0]['membership_id'], 'a2')
        self.assertEqual(f_mem_a.iloc[0]['start_date'],
            datetime.date(2005, 1, 1))
        self.assertEqual(f_mem_a.iloc[0]['end_date'],
            datetime.date(2005, 12, 31))

        self.assertEqual(f_mem_a.iloc[-1]['person_id'], 'p2')
        self.assertEqual(f_mem_a.iloc[-1]['membership_id'], 'a7')
        self.assertEqual(f_mem_a.iloc[-1]['start_date'],
            datetime.date(2010, 1, 1))
        self.assertEqual(f_mem_a.iloc[-1]['end_date'],
            datetime.date(2010, 12, 31))

    def test_filter_dates_includes_rows_enclosing_dates(self):

        f_mem_a = filter.filter_dates(
            mem_a,
            start_col='start_date',
            end_col='end_date',
            from_date='2005-06-30',
            to_date='2005-06-30')

        self.assertEqual(f_mem_a.shape[0], 2)
        self.assertEqual(f_mem_a.shape[1], mem_a.shape[1])

        self.assertEqual(f_mem_a.iloc[0]['person_id'], 'p1')
        self.assertEqual(f_mem_a.iloc[0]['membership_id'], 'a2')
        self.assertEqual(f_mem_a.iloc[0]['start_date'],
            datetime.date(2005, 1, 1))
        self.assertEqual(f_mem_a.iloc[0]['end_date'],
            datetime.date(2005, 12, 31))

        self.assertEqual(f_mem_a.iloc[1]['person_id'], 'p2')
        self.assertEqual(f_mem_a.iloc[1]['membership_id'], 'a5')
        self.assertEqual(f_mem_a.iloc[1]['start_date'],
            datetime.date(2005, 1, 1))
        self.assertEqual(f_mem_a.iloc[-1]['end_date'],
            datetime.date(2005, 12, 31))

# Test filter_memberships -----------------------------------------------------

class TestFilterMemberships(unittest.TestCase):

    """
    Test that filter_memberships returns a DataFrame with the expected
    properties.

    """

    def test_that_filter_dates_raises_missing_column_error(self):

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_memberships(
                tm=mem_a,
                fm=mem_b,
                tm_id_col='no_such_column',
                tm_start_col='start_date',
                tm_end_col='end_date',
                fm_start_col='start_date',
                fm_end_col='end_date',
                join_col='person_id')

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_memberships(
                tm=mem_a,
                fm=mem_b,
                tm_id_col='membership_id',
                tm_start_col='no_such_column',
                tm_end_col='end_date',
                fm_start_col='start_date',
                fm_end_col='end_date',
                join_col='person_id')

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_memberships(
                tm=mem_a,
                fm=mem_b,
                tm_id_col='membership_id',
                tm_start_col='start_date',
                tm_end_col='no_such_column',
                fm_start_col='start_date',
                fm_end_col='end_date',
                join_col='person_id')

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_memberships(
                tm=mem_a,
                fm=mem_b,
                tm_id_col='membership_id',
                tm_start_col='start_date',
                tm_end_col='end_date',
                fm_start_col='no_such_column',
                fm_end_col='end_date',
                join_col='person_id')

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_memberships(
                tm=mem_a,
                fm=mem_b,
                tm_id_col='membership_id',
                tm_start_col='start_date',
                tm_end_col='end_date',
                fm_start_col='start_date',
                fm_end_col='no_such_column',
                join_col='person_id')

        with self.assertRaises(errors.MissingColumnError):

            f_mem_a = filter.filter_memberships(
                tm=mem_a,
                fm=mem_b,
                tm_id_col='membership_id',
                tm_start_col='start_date',
                tm_end_col='end_date',
                fm_start_col='start_date',
                fm_end_col='end_date',
                join_col='no_such_column')

    def test_that_filter_memberships_filters_correct_memberships(self):

        f_mem_a = filter.filter_memberships(
            tm = mem_a,
            fm = mem_b,
            tm_id_col='membership_id',
            tm_start_col='start_date',
            tm_end_col='end_date',
            fm_start_col='start_date',
            fm_end_col='end_date',
            join_col='person_id')

        self.assertEqual(f_mem_a.shape[0], 4)
        self.assertEqual(f_mem_a.shape[1], mem_a.shape[1])
        self.assertEqual((f_mem_a.columns == mem_a.columns).all(), True)

        self.assertEqual((f_mem_a['person_id'] == [
            'p1', 'p1', 'p2', 'p2']).all(), True)

        self.assertEqual((f_mem_a['membership_id'] == [
            'a1', 'a3', 'a6', 'a8']).all(), True)

        self.assertEqual((f_mem_a['start_date'] == [
            datetime.date(2001, 1, 1),
            datetime.date(2006, 1, 1),
            datetime.date(2006, 1, 1),
            datetime.date(2015, 1, 1)]).all(), True)

        self.assertEqual((f_mem_a['end_date'] == [
            datetime.date(2001, 12, 31),
            datetime.date(2006, 12, 31),
            datetime.date(2006, 12, 31),
            datetime.date(2015, 12, 31)]).all(), True)
