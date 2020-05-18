from typing import List


class Site(object):
    """Contains configuration for a site."""

    def __init__(self, name: str, bidders: List[str], floor: float):
        self.name = name
        self.bidders = bidders
        self.floor = floor

    def __eq__(self, other):
        if not isinstance(other, Site):
            return NotImplemented

        return self.name == other.name and \
            self.bidders == other.bidders and \
            self.floor == other.floor


class Bidder(object):
    """Contains configuration for a bidder."""

    def __init__(self, name: str, adjustment: float):
        self.name = name
        self.adjustment = adjustment

    def __eq__(self, other):
        if not isinstance(other, Bidder):
            return NotImplemented

        return self.name == other.name and \
            self.adjustment == other.adjustment


class Config(object):
    """Contains all configuration for the Auction module."""

    def __init__(self, sites: List[Site], bidders: List[Bidder]):
        self.sites = sites
        self.bidders = bidders

    def __eq__(self, other):
        if not isinstance(other, Config):
            return NotImplemented

        return self.sites == other.sites and \
            self.bidders == other.bidders
