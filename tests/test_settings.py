# -*- coding: utf-8 -*-
"""Test settings functions."""

# Imports ---------------------------------------------------------------------

import unittest

import pdpy.constants as constants
import pdpy.settings as settings

# Test get_api_url ------------------------------------------------------------

class GetApiUrl(unittest.TestCase):

    """
    Test that get_api_url returns default url when a url has not been set.

    """

    def test_that_get_api_url_returns_default_url(self):

        self.assertEqual(
            settings.get_api_url(),
            constants.SETTINGS_API_URL_DEFAULT)

# Test set_api_url ------------------------------------------------------------

class SetApiUrl(unittest.TestCase):

    """
    Test that set_api_url sets the api url returned by get_api_url.

    """

    def test_that_set_api_url_sets_api_url(self):

        api_url = 'http://localhost:8000/sparql'
        settings.set_api_url(api_url)
        self.assertEqual(settings.get_api_url(), api_url)
        settings.set_api_url(constants.SETTINGS_API_URL_DEFAULT)
        self.assertEqual(
            settings.get_api_url(),
            constants.SETTINGS_API_URL_DEFAULT)

# Test reset_api_url ----------------------------------------------------------

class ResetApiUrl(unittest.TestCase):

    """
    Test that reset_api_url resets the api url returned by get_api_url.

    """

    def test_that_reset_api_url_resets_api_url(self):

        api_url = 'http://localhost:8000/sparql'
        settings.set_api_url(api_url)
        self.assertEqual(settings.get_api_url(), api_url)
        settings.reset_api_url()
        self.assertEqual(
            settings.get_api_url(),
            constants.SETTINGS_API_URL_DEFAULT)
