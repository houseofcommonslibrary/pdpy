# pdpy

pdpy is a Python package for downloading data from the UK Parliament's data platform. An equivalent package is available for R called [pdpr](https://github.com/olihawkins/pdpr).

## Overview

The UK Parliament's data platform contains data on Parliamentary activity. It underpins Parliament's new website, which is being developed at [beta.parliament.uk](https://beta.parliament.uk). Data in the platform is stored as RDF and is available through a SPARQL endpoint. You can see the structure of the vocabulary for the data visualised with [WebVOWL](http://visualdataweb.de/webvowl/#iri=https://raw.githubusercontent.com/ukparliament/Ontology/master/Ontology.ttl).

This package provides access to data stored in the data platform through two interfaces at different levels:

* A low-level interface that takes takes a SPARQL SELECT query, sends it to the platform, and returns the result as a [pandas](http://pandas.pydata.org) DataFrame, with data types appropriately converted.

* A high-level interface comprising families of functions for downloading specific datasets, whose contents can be customised through function arguments. In some cases these higher level functions can additionally process the data to make it more suitable for analysis.

The higher-level interface currently focuses on providing key data about Members of both Houses of Parliament, but you can use the lower level interface to send custom queries of your own for other data.

### Installation

Install from PyPI using pip:
```sh
pip install pdpy
```

## Package conventions

There are certain conventions that apply across the package.

Functions that makes calls to the data platform (or to other online resources) are prefixed `fetch_*`, while those that retrieve or generate data locally are prefixed `get_*`.

Column names used in dataframes returned by higher-level functions reflect the terms used for those data items in the UK Parliament RDF vocabulary, but modified so that the `camelCase` of RDF is replaced with the `lowercase_and_underscores` used in Python. This means that column names can sometimes be long, but I think maintaining a transparent relationship between the data returned by the package and the data stored in the platform makes both the package and platform more useful.

Higher-level functions always return columns containing the ids of the entities represented in the data to help with grouping, summarising, and linking between datasets. This can make the dataframes harder to browse in an interactive shell. To make this easier, the package has a function called `readable` that returns a copy of the dataframe with any id columns removed.

``` python
import pdpy
mps = pdpy.fetch_mps()
pdpy.readable(mps)
```

## Package status

This package is currently in _beta_. This partly reflects the fact that the data platform is still evolving but mainly reflects the fact that this package is still young. Over time new sets of functions will be added to access other datasets and more established parts of the package API will be declared stable. But right now it's all beta.

## Roadmap

* Further analysis functions for data on MPs and Lords
* Caching
* Written Questions and Answers API
* New APIs for new datasets in future

## Contributions

I welcome any feedback, bug reports, and suggestions for improvement. Please talk to me before submitting a pull request. There are potentially a very large number of features that could be added to the package and I want to make sure it evolves with a consistent set of interfaces that share common design patterns. The package also has an R sibling, and I aim to maintain feature parity across both languages.

## Query API

__sparql_select__(_query_)

The low-level query API consists of a single function which takes a SPARQL SELECT query, sends it to the data platform, and returns the results as a pandas DataFrame.

```python
query = """
    PREFIX : <https://id.parliament.uk/schema/>
    SELECT * WHERE { ?p ?s ?o . } LIMIT 1
"""

result = pdpy.sparql_select(query)
result.iloc[0]

# Output:
# p      http://www.w3.org/1999/02/22-rdf-syntax-ns#type
# s      http://www.w3.org/1999/02/22-rdf-syntax-ns#type
# o      http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
# Name: 0, dtype: object
```

The function will try to convert data types it recognises to native Python types. Currently, it converts XML dates to _datetime.date_ objects and returns all other values as strings. New data types may be added as they are encountered in expanding the higher level api.

## Members API

The Members API provides access to data on Members of both Houses of Parliament. It provides similar functions for downloading data on both MPs and Lords, but the structure of the data returned in each case may differ to reflect differences between Commons and Lords memberships.

Each of these Member functions can take optional arguments for a `from_date` and a `to_date`, which can be used to filter the rows returned based on a period of activity related to each row. The on_date argument is a convenience that sets the `from_date` and `to_date` to the same given date. The `on_date` has priority: if the `on_date` is set, the `from_date` and `to_date` are ignored. The values for these arguments can be either a _datetime.date_ or a string specifying a date in ISO 8601 format ('YYYY-MM-DD').

The filtering performed using these arguments is inclusive: a row is returned if any part of the activity in question falls within the period specified with the from and to dates. If the activity in question has not yet ended, the end date will have a value of NumPy.NaN.


### MPs

Some MP functions have an optional argument called `while_mp`, which filters the data to include only those rows that coincide with the period when the individual was serving in the House of Commons. This is sometimes necessary because someone who serves in the House of Commons may later serve in the House of Lords and may hold government roles or committee memberships while serving in both Houses. When this argument is set to _False_ these functions will return all relevant records for each individual, even if the records themselves relate to periods when the individual was not an MP.

_pdpy_.__fetch_mps__(_from_date=None_, _to_date=None_, _on_date = NA_)

Fetch a dataframe of key details about each MP, with one row per MP.

This dataframe contains summary details for each MP, such as names, gender, and dates of birth and death.

The `from_date`, `to_date` and `on_date` arguments can be used to filter the MPs returned based on the dates of their Commons memberships. Note that in this particular case the filtering does not rely on dates shown in the dataframe but uses Commons membership records to calculate whether an MP was serving on the dates in question. While breaks in service are therefore accounted for, this function does not yet have an option to exclude serving Members who were prevented from sitting at a given point in time for some reason.

_pdpy_.__fetch_commons_memberships__(_from_date=None_, _to_date=None_, _on_date = NA_)

Fetch a dataframe of Commons memberships for each MP, with one row per Commons membership.

The memberships dates are processed to impose consistent rules on the start and end dates for memberships. Specifically, Commons memberships are taken to end at the dissolution of each Parliament, rather than on the date of the general election at which an MP was defeated.

_pdpy_.__fetch_mps_party_memberships__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_mp=True_, _collapse=False_)

Fetch a dataframe of party memberships for each MP, with one row per party membership.

The `collapse` argument determines whether to collapse consecutive memberships within the same party into a single period of continuous party membership. The default value of this argument is _False_, but it can be useful sometimes because some Members' party memberships have been recorded separately for each Parliament, even when they haven't changed party. Setting this value to _True_ is helpful when you want to identify Members who have changed party allegiance. Note that setting this value to _True_ means that party membership ids are not returned in the dataframe, as individual party memberships are combined.

Note that party memberships are not necessarily closed when an individual stops being an MP.

_pdpy_.__fetch_mps_government_roles__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_mp=True_)

Fetch a dataframe of government roles for each MP, with one row per government role.

_pdpy_.__fetch_mps_opposition_roles__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_mp=True_)

Fetch a dataframe of opposition roles for each MP, with one row per opposition role.

_pdpy_.__fetch_mps_commitee_memberships__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_mp=True_)

Fetch a dataframe of  Parliamentary committee memberships for each MP, with one row per committee membership.

### Lords

Some Lords functions have an optional argument called `while_lord`, which filters the rows to include only those records that coincide with the period when the individual was serving in the House of Lords. This is sometimes necessary because someone who serves in the House of Lords may previously have served in the House of Commons and may have held government roles or committee memberships while serving in both Houses. When this argument is set to _False_ these functions will return all relevant records for each individual, even if the records themselves relate to periods when the individual was not a Lord.

_pdpy_.__fetch_lords__(_from_date=None_, _to_date=None_, _on_date = NA_)

Fetch a dataframe of key details about each Lord, with one row per Lord.

This dataframe contains summary details for each Lord, such as names, gender, and dates of birth and death.

The `from_date`, `to_date` and `on_date` arguments can be used to filter the Lords returned based on the dates of their Lords memberships. Note that in this particular case the filtering does not rely on dates shown in the dataframe but uses Lords membership records to calculate whether a Lord was serving on the dates in question. While breaks in service are therefore accounted for, this function does not yet have an option to exclude serving Members who were prevented from sitting at a given point in time for some reason.

_pdpy_.__fetch_lords_memberships__(_from_date=None_, _to_date=None_, _on_date = NA_)

Fetch a dataframe of Commons memberships for each Lord, with one row per Lords membership.

_pdpy_.__fetch_lords_party_memberships__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_lord=True_, _collapse=False_)

Fetch a dataframe of party memberships for each Lord, with one row per party membership.

The `collapse` argument determines whether to collapse consecutive memberships within the same party into a single period of continuous party membership. The default value of this argument is _False_, but it can be useful sometimes because some Members' party memberships have been recorded separately for each Parliament, even when they haven't changed party. Setting this value to _True_ is helpful when you want to identify Members who have changed party allegiance. Note that setting this value to _True_ means that party membership ids are not returned in the dataframe, as individual party memberships are combined.

Note that party memberships are not necessarily closed when an individual stops being a Lord.

_pdpy_.__fetch_lords_government_roles__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_lord=True_)

Fetch a dataframe of government roles for each Lord, with one row per government role.

_pdpy_.__fetch_lords_opposition_roles__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_lord=True_)

Fetch a dataframe of opposition roles for each Lord, with one row per opposition role.

_pdpy_.__fetch_lords_commitee_memberships__(_from_date=None_, _to_date=None_, _on_date = NA_, _while_lord=True_)

Fetch a dataframe of Parliamentary committee memberships for each Lord, with one row per committee membership.
