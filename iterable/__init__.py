"""
python-iterable
--------------
Iterable API python client.
:copyright: (c) 2016 by SteelSeries
:license: MIT. See LICENSE for more details
"""

__title__ = 'iterable'
__version__ = '0.0.1'
__author__ = 'Eric Burns'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 SteelSeries'


# Configuration variables

api_key = None
api_base = 'https://api.iterable.com/api/'


# Resource

from iterable.resource import (
    Commerce,
    List,
    User,
    Workflow,
)

# Models

from iterable.models import (
    CommerceItem,
)
