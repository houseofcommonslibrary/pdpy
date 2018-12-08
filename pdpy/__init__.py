"""pdpr: A package for downloading data from the Parliamentary Data Platform.

The pdpr package provides a suite of functions for downloading data from
the data platform for the UK Parliament.
"""

from . import core
from .core import sparql_select

from . import elections
from .elections import get_general_elections
from .elections import get_general_elections_dict

from . import lords
from .lords import fetch_lords
from .lords import fetch_lords_memberships
from .lords import fetch_lords_party_memberships
from .lords import fetch_lords_government_roles
from .lords import fetch_lords_opposition_roles
from .lords import fetch_lords_committee_memberships

from . import mps
from .mps import fetch_mps
from .mps import fetch_commons_memberships
from .mps import fetch_mps_party_memberships
from .mps import fetch_mps_government_roles
from .mps import fetch_mps_opposition_roles
from .mps import fetch_mps_committee_memberships

from . import utils
from .utils import readable
