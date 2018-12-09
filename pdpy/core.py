# -*- coding: utf-8 -*-
"""Core download functions."""

# Imports ---------------------------------------------------------------------

import datetime
import json
import numpy as np
import pandas as pd
import requests

from . import constants
from . import errors

# Functions  ------------------------------------------------------------------

def request(query):

    """Send an http request with a query and return the response.

    request sends a SPARQL query to the api endpoint and returns the response
    object. It is a simple wrapper around request.post. It sets the appropriate
    headers and sends the query as the request body. It does not validate the
    query or handle the response in any way. The response format is JSON.

    Parameters
    ----------
    query : str
        A SPARQL query as a string.

    Returns
    -------
    out : Response
        The http response object from requests.

    """

    url = 'https://api.parliament.uk/sparql'
    headers = {}
    headers['content-type'] = 'application/sparql-query'
    headers['accept'] = 'application/sparql-results+json'
    response = requests.post(url, headers=headers, data=query)
    return response


def sparql_select(query):

    """Send a select query and return the response as a DataFrame.

    sparql_select sends a SPARQL query to the api endpoint and returns the
    response as a DataFrame. The SPARQL should be a SELECT query as the
    response is processed as tabular data. The function will convert datatypes
    that it recognises. It currently recognises date types. All other data
    returned in the DataFrame will be strings. If the query syntax is not valid
    or the request fails for any other reason a RequestError will be raised
    with the response text.

    Parameters
    ----------
    query : str
        A SPARQL SELECT query as a string.

    Returns
    -------
    out : DataFrame
        A pandas dataframe containing the results of the query.

    """

    # Send the query and get the response
    response = request(query)

    # If the server returned an error raise it with the response text
    if not response.ok:
        raise errors.RequestError(response.text)

    # Process the response as tabular data and return it as a DataFrame
    json = response.json()
    rows = []
    headers = json['head']['vars']
    records = json['results']['bindings']

    # For each record build a row and assign values based on the data type
    for record in records:
        row = []
        for header in headers:
            if header in record:
                if 'datatype' in record[header] and \
                        record[header]['datatype'] == constants.XML_DATE:

                    row.append(
                        datetime.datetime.strptime(
                        record[header]['value'], '%Y-%m-%d+%H:%M').date())
                else:
                    row.append(record[header]['value'].strip())
            else:
                row.append(None)
        rows.append(row)

    return pd.DataFrame(data=rows, columns=headers).fillna(value=np.NaN)
