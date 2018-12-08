# -*- coding: utf-8 -*-
"""Test elections data functions."""

# Imports ---------------------------------------------------------------------

import datetime
import numpy as np
import pandas as pd
import unittest

import pdpy.elections as elections

# Tests -----------------------------------------------------------------------

class TestGetGeneralElections(unittest.TestCase):

    """
    Test that get_general_elections returns the expected elections data.

    """

    def test_get_general_elections(self):

        ge = elections.get_general_elections()

        self.assertEqual(list(ge), ['name', 'dissolution', 'election'])
        self.assertEqual(ge['name'].dtype, np.dtype('O'))
        self.assertEqual(ge['dissolution'].dtype, np.dtype('O'))
        self.assertEqual(ge['election'].dtype, np.dtype('O'))
        self.assertIsInstance(ge['name'][0], str)
        self.assertIsInstance(ge['dissolution'][0], datetime.date)
        self.assertIsInstance(ge['election'][0], datetime.date)

        # Test that dissolutions always precede elections
        self.assertTrue(
            (ge['dissolution'] < ge['election']).all())

        # Test that elections always precede the following dissolution
        self.assertTrue((
            ge['election'][:-1].reset_index(drop=True) <
            ge['dissolution'][1:].reset_index(drop=True)
        ).all())

        # Test that election names are unique
        self.assertTrue(
            len(ge['name']) == len(ge['name'].unique()))


class TestGetGeneralElectionsDict(unittest.TestCase):

    """
    Test that get_general_elections_dict returns the expected elections data.

    """

    def test_get_general_elections_dict(self):

        ge = elections.get_general_elections_dict()

        for e in ge.values():
            self.assertEqual(len(e.keys()), 2)
            self.assertIn('election', list(e.keys()))
            self.assertIn('dissolution', list(e.keys()))
            self.assertIsInstance(e['dissolution'], datetime.date)
            self.assertIsInstance(e['election'], datetime.date)
            self.assertTrue(e['dissolution'] < e['election'])
