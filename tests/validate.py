# -*- coding: utf-8 -*-
"""Manage test data for validation."""

# Imports ---------------------------------------------------------------------

import os
import pandas as pd

# Constants -------------------------------------------------------------------

TEST_DATA_DIR = os.path.join('tests', 'data')

# Read and write data ---------------------------------------------------------

def read(filename):
    """Read a file from the data directory."""
    return pd.read_pickle(
        os.path.join(TEST_DATA_DIR, '{0}.pkl'.format(filename)))

def write(df, filename):
    """Write a dataframe to the data directory."""
    df.to_pickle(os.path.join(TEST_DATA_DIR, '{0}.pkl'.format(filename)))

# Comparison function ---------------------------------------------------------

def compare_obs_exp(self, obs, exp, cols):

    """Compare two dataframes on structure and contents of selected columns."""

    self.assertEqual(obs.shape[0], exp.shape[0])
    self.assertEqual(obs.shape[1], exp.shape[1])
    self.assertTrue((obs.columns == exp.columns).all())

    for col in cols:
        self.assertTrue((obs[col] == exp[col]).all())
