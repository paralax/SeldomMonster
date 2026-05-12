#!/usr/bin/env python3

import json

from pycti import OpenCTIApiClient

from settings import (OPENCTI_URL, OPENCTI_KEY)

opencti = OpenCTIApiClient(OPENCTI_URL, OPENCTI_KEY)

"""
search_term = "www-mondial-coursier.com" # "121.167.125.180"
data = opencti.stix_cyber_observable.list(search=search_term)
"""

custom_attributes = """
        id
        name
        published
        description
        """
num=3
data = opencti.report.list(first=num, orderby="published", customAttributes=custom_attributes, orderMode="asc")

print(json.dumps(data, indent=4))
