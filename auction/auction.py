from typing import List, Dict
import json

from .config import Config


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


class AuctionHelper(object):
    """Contains helper methods for calculating winning bids for an auction."""

    def __init__(self, config: Config):
        self._config = config

        # TODO: Find a better way to do a .ToDictionary() equivalent in python
        self._bidder_adjustments: Dict[str, float] = {}
        for bidder in config.bidders:
            self._bidder_adjustments[bidder.name] = bidder.adjustment

    def get_winning_bids(self, auction: Auction) -> List[Bid]:
        """Get winning bids.

        :param auction: The auction to perform winning big computation on.
        :return: Returns a list of winnings bids (per unit) for the auction.
        """
        winning_bids: List[Bid] = []

        print("doing auction for site " + auction.site)

        # Get configuration for the current site based on the auction name.
        site_config = next(
            filter(lambda i: i.name == auction.site, self._config.sites))

        for unit in auction.units:
            unit_bids = list(filter(lambda i: i.unit == unit and
                                    i.bidder in site_config.bidders,
                                    auction.bids))

            # Adjustments, though based on averages, are estimates. The floor
            # should only be calculated based on the actual bid, not the payout.
            unit_bids = list(filter(lambda i:
                                    i.bid >= site_config.floor,
                                    unit_bids))

            # Order the bids by their adjusted value.
            sortedBids = sorted(unit_bids, key=self.get_adjusted_value,
                                reverse=True)

            # TODO: What if the list is empty?
            winning_bids.append(sortedBids[0])

        return winning_bids

    def get_adjusted_value(self, bid: Bid):
        return bid.bid + (bid.bid * self._bidder_adjustments[bid.bidder])
