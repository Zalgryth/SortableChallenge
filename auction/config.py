from typing import List


class Site(object):
    """Contains configuration for a site."""

    def __init__(self, name: str, bidders: List[str], floor: float):
        self.name = name
        self.bidders = bidders
        self.floor = floor


class Bidder(object):
    """Contains configuration for a bidder."""

    def __init__(self, name: str, adjustment: float):
        self.name = name
        self.adjustment = adjustment


class Config(object):
    """Contains all configuration for the Auction module."""

    def __init__(self, sites: List[Site], bidders: List[Bidder]):
        self.sites = sites
        self.bidders = bidders
