from typing import List, Dict
import json

from .config import Config


class Bid(object):
    """A bid from a bidder for a specific unit."""

    def __init__(self, bidder: str, unit: str, bid: float):
        self.bidder = bidder
        self.bid = bid
        self.unit = unit

    def __eq__(self, other):
        if not isinstance(other, Bid):
            return NotImplemented

        return self.bidder == other.bidder and \
            self.bid == other.bid and \
            self.unit == other.unit


class Auction(object):
    """An auction request for a site with a list of available bids."""

    def __init__(self, site: str, units: List[str], bids: List[Bid]):
        self.site = site
        self.units = units
        self.bids = bids

    def __eq__(self, other):
        if not isinstance(other, Auction):
            return NotImplemented

        return self.site == other.site and \
            self.units == other.units and \
            self.bids == other.bids


class AuctionHelper(object):
    """Contains helper methods for calculating winning bids for an auction."""

    def __init__(self, config: Config):
        self._config = config

        self._bidder_adjustments = dict(
            (x.name, x.adjustment) for x in config.bidders)

    def get_winning_bids(self, auction: Auction) -> List[Bid]:
        """Get winning bids.

        :param auction: The auction to perform winning bid computation on.
        :return: Returns a list of winnings bids (per unit) for the auction.
        """
        winning_bids: List[Bid] = []

        # Get configuration for the current site based on the auction name.
        site_config = next(
            filter(lambda i: i.name == auction.site, self._config.sites), None)

        # No site config was found for the auction... Return the empty list.
        if site_config is None:
            return winning_bids

        for unit in auction.units:
            unit_bids = list(filter(lambda i: i.unit == unit and
                                    i.bidder in site_config.bidders and
                                    i.bidder in self._bidder_adjustments.keys() and
                                    i.bid >= 0,
                                    auction.bids))

            # The bid value must be greater than the floor after adjustments.
            unit_bids = list(filter(lambda i:
                                    self.get_adjusted_value(
                                        i) >= site_config.floor,
                                    unit_bids))

            # Order the bids by their adjusted value.
            sorted_bids = sorted(unit_bids, key=self.get_adjusted_value,
                                 reverse=True)

            # If there are no winning bids, don't add to the list.
            if len(sorted_bids) > 0:
                winning_bids.append(sorted_bids[0])

        return winning_bids

    def get_adjusted_value(self, bid: Bid):
        return bid.bid + (bid.bid * self._bidder_adjustments[bid.bidder])
