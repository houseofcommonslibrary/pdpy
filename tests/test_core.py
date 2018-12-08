# -*- coding: utf-8 -*-
"""Test core download functions."""

# Imports ---------------------------------------------------------------------

import datetime
import numpy as np
import pandas as pd
import requests
import time
import unittest
import warnings

import pdpy.constants as constants
import pdpy.core as core
import pdpy.errors as errors
import pdpy.utils as utils

# Setup -----------------------------------------------------------------------

# Check api is available
api_available = utils.check_api()

# Queries ---------------------------------------------------------------------

query_basic = """
    PREFIX : <https://id.parliament.uk/schema/>
    SELECT *
    WHERE {
        ?p ?s ?o .
    }
    LIMIT 1
"""

query_person = """
    PREFIX : <https://id.parliament.uk/schema/>
    PREFIX d: <https://id.parliament.uk/>
    SELECT DISTINCT

        ?person
        ?given_name
        ?family_name
        ?gender
        ?dob

    WHERE {

        # Entity id for Shirley Williams
        BIND(d:URDlhhkg AS ?person)

        ?person :personGivenName ?given_name ;
            :personFamilyName ?family_name ;
            :personHasGenderIdentity/:genderIdentityHasGender/:genderName ?gender .
        OPTIONAL { ?person :personDateOfBirth ?dob . }
    }
"""

query_broken = """
    PREFIX : <https://id.parliament.uk/schema/>
    # PREFIX d: <https://id.parliament.uk/> Commented out to break query
    SELECT DISTINCT

        ?person
        ?given_name
        ?family_name
        ?gender
        ?dob

    WHERE {

        # Entity id for Shirley Williams
        BIND(d:URDlhhkg AS ?person)

        ?person :personGivenName ?given_name ;
            :personFamilyName ?family_name ;
            :personHasGenderIdentity/:genderIdentityHasGender/:genderName ?gender .
        OPTIONAL { ?person :personDateOfBirth ?dob . }
    }
"""

query_broken_error = "{}{}".format(
    'MALFORMED QUERY: org.eclipse.rdf4j.query.parser.sparql.ast.',
    'VisitorException: QName \'d:URDlhhkg\' uses an undefined prefix')

# Tests -----------------------------------------------------------------------

class TestRequestBasic(unittest.TestCase):

    """Test that request sends and receives the most basic SPARQL query."""

    def setUp(self):
        if not api_available:
            self.skipTest('api could not be reached')

    def test_request_basic(self):

        # Suppress the warning for the broken socket
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)

            response = core.request(query_basic)
            json = response.json()
            headers = json['head']['vars']
            records = json['results']['bindings']

            self.assertTrue(response.ok)
            self.assertEqual(headers, ['p', 's', 'o'])
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['p']['value'],
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
            self.assertEqual(records[0]['s']['value'],
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
            self.assertEqual(records[0]['o']['value'],
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')

        time.sleep(constants.API_PAUSE_TIME)


class TestRequestPerson(unittest.TestCase):

    """Test that request sends and receives a Parliamentary query."""

    def setUp(self):
        if not api_available:
            self.skipTest('api could not be reached')

    def test_request_person(self):

        # Suppress the warning for the broken socket
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)

            response = core.request(query_person)
            json = response.json()
            headers = json['head']['vars']
            records = json['results']['bindings']

            self.assertTrue(response.ok)
            self.assertEqual(headers,
                ['person', 'given_name', 'family_name', 'gender', 'dob'])
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['person']['value'],
                'https://id.parliament.uk/URDlhhkg')
            self.assertEqual(records[0]['given_name']['value'], 'Shirley')
            self.assertEqual(records[0]['family_name']['value'], 'Williams')
            self.assertEqual(records[0]['gender']['value'], 'Female')
            self.assertEqual(records[0]['dob']['value'], '1930-07-27+01:00')
            self.assertEqual(records[0]['dob']['datatype'], constants.XML_DATE)

        time.sleep(constants.API_PAUSE_TIME)


class TestSelectBasic(unittest.TestCase):

    """Test that select returns data for the most basic SPARQL query."""

    def setUp(self):
        if not api_available:
            self.skipTest('api could not be reached')

    def test_select_basic(self):

        # Suppress the warning for the broken socket
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)

            data = core.sparql_select(query_basic)

            self.assertEqual(list(data), ['p', 's', 'o'])
            self.assertEqual(data['p'].dtype, np.dtype('O'))
            self.assertEqual(data['s'].dtype, np.dtype('O'))
            self.assertEqual(data['o'].dtype, np.dtype('O'))
            self.assertEqual(data.shape, (1, 3))
            self.assertIsInstance(data['p'][0], str)
            self.assertIsInstance(data['s'][0], str)
            self.assertIsInstance(data['o'][0], str)
            self.assertEqual(data['p'][0],
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
            self.assertEqual(data['s'][0],
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
            self.assertEqual(data['o'][0],
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')

        time.sleep(constants.API_PAUSE_TIME)


class TestSelectPerson(unittest.TestCase):

    """Test that select returns data for a Parliamentary query."""

    def setUp(self):
        if not api_available:
            self.skipTest('api could not be reached')

    def test_select_person(self):

        # Suppress the warning for the broken socket
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)

            data = core.sparql_select(query_person)

            self.assertEqual(list(data),
                ['person', 'given_name', 'family_name', 'gender', 'dob'])
            self.assertEqual(data['person'].dtype, np.dtype('O'))
            self.assertEqual(data['given_name'].dtype, np.dtype('O'))
            self.assertEqual(data['family_name'].dtype, np.dtype('O'))
            self.assertEqual(data['gender'].dtype, np.dtype('O'))
            self.assertEqual(data['dob'].dtype, np.dtype('O'))
            self.assertEqual(data.shape, (1, 5))
            self.assertIsInstance(data['person'][0], str)
            self.assertIsInstance(data['given_name'][0], str)
            self.assertIsInstance(data['family_name'][0], str)
            self.assertIsInstance(data['gender'][0], str)
            self.assertIsInstance(data['dob'][0], datetime.date)
            self.assertEqual(data['person'][0],
                'https://id.parliament.uk/URDlhhkg')
            self.assertEqual(data['given_name'][0], 'Shirley')
            self.assertEqual(data['family_name'][0], 'Williams')
            self.assertEqual(data['gender'][0], 'Female')
            self.assertEqual(data['dob'][0], datetime.date(1930, 7, 27))

        time.sleep(constants.API_PAUSE_TIME)


class TestSelectBroken(unittest.TestCase):

    """Test that select raises a request error for a broken query."""

    def setUp(self):
        if not api_available:
            self.skipTest('api could not be reached')

    def test_select_broken(self):

        # Suppress the warning for the broken socket
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)

            with self.assertRaises(errors.RequestError) as cm:
                data = core.sparql_select(query_broken)

            request_exception = cm.exception
            self.assertEqual(request_exception.response, query_broken_error)

        time.sleep(constants.API_PAUSE_TIME)
