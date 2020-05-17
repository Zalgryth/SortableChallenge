from typing import List


class Bid(object):
    """A bid from a bidder for a specific unit."""

    def __init__(self, bidder: str, unit: str, bid: float):
        self.bidder = bidder
        self.bid = bid
        self.unit = unit


class Auction(object):
    """An auction request for a site with a list of available bids."""

    def __init__(self, site: str, units: List[str], bids: List[Bid]):
        self.site = site
        self.units = units
        self.bids = bids
