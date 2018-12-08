# -*- coding: utf-8 -*-
"""Package errors."""

class Error(Exception):

    """Base class for exceptions in this module."""
    pass


class RequestError(Error):

    """Exception raised for errors with http requests. Typically these are the
    result of malformed SPARQL queries.

    Parameters
    ----------
    response : str
        The text of the server reponse.

    """

    def __init__(self, response):
        message = ('The server responded with the following message: '
            '{0}'.format(response))
        super(RequestError, self).__init__(message)
        self.message = message
        self.response = response


class DateFormatError(Error):

    """Exception raised for errors parsing date strings.

    Parameters
    ----------
    date_str : str
        The date string that could not be parsed.

    """

    def __init__(self, date_str):
        message = (
            'Could not parse \'{0}\' as a date: '
            'use format \'YYYY-MM-DD\''.format(date_str))
        super(DateFormatError, self).__init__(message)
        self.message = message
        self.date_str = date_str


class MissingColumnError(Error):

    """Exception raised for errors handling dataframes with missing columms.

    Parameters
    ----------
    colname : str
         The name of the column that could not be found.

    """

    def __init__(self, colname):
        message = ('Could not find a column called \'{0}\''.format(colname))
        super(MissingColumnError, self).__init__(message)
        self.message = message
        self.colname = colname
