# -*- coding: utf-8 -*-
"""User configurable package settings."""

# Imports ---------------------------------------------------------------------

from . import constants

# Settings dictionary ---------------------------------------------------------

settings = {}

# Settings: api url -----------------------------------------------------------

def get_api_url():

    """Get the api url.

    get_api_url gets the url that the package is currently configured to use
    for the SPARQL endpoint to a data platform instance.

    Returns
    -------
    out : str
        The currently set api url as a string.

    """

    if constants.SETTINGS_API_URL not in settings:
        set_api_url(constants.SETTINGS_API_URL_DEFAULT)

    return  settings[constants.SETTINGS_API_URL]


def set_api_url(api_url):

    """Set the api url.

    set_api_url sets the url that the package uses for the api endpoint. By
    default the package uses the main live endpoint for the data platform's
    SPARQL api. If you wish to run a local version of the api you can use this
    function to tell the package to use that endpoint instead.

    Parameters
    ----------
    api_url : str
        The url of an available data platform SPARQL endpoint.

    Returns
    -------
    out : None

    """

    settings[constants.SETTINGS_API_URL] = api_url


def reset_api_url():

    """Reset the api url to the default.

    reset_api_url resets the url that the package uses for the api endpoint to
    the live api url.

    """

    set_api_url(constants.SETTINGS_API_URL_DEFAULT)
