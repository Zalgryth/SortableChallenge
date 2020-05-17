#!usr/bin/env python3
import sys
import json
import pathlib
from typing import List, Dict

from . import json_encoder
from .auction import Auction, Bid
from .config import Config, Bidder, Site


def main():
    config = get_config()
    auctions = getAuctions()

    winning_bids: List[Bid] = []

    for auction in auctions:
        winning_bids.append(get_winning_bids(auction, config))

    print_json(winning_bids)


def print_json(data):
    """Prints JSON using the default encoder.

    Parameters:
    argument1 (int): Description of arg1

    """
    print(json.dumps(data, indent=4, cls=json_encoder.DefaultEncoder))


def get_winning_bids(auction: Auction, config: Config) -> List[Bid]:
    """

    :param auction:
    :param config:
    :return:
    """
    # return an array of winning bids for the auction
    winning_bids: List[Bid] = []

    print("doing auction for site " + auction.site)

    # Get configuration for the current site based on the auction name.
    site_config = next(filter(lambda i: i.name == auction.site, config.sites))

    # TODO: Find a better way to do a .ToDictionary() equivalent in python
    bidder_adjustments = {}
    for bidder in config.bidders:
        bidder_adjustments[bidder.name] = bidder.adjustment

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
        sortedBids = sorted(unit_bids,
                            key=lambda x:
                            get_adjusted_value(x, bidder_adjustments),
                            reverse=True)

        print("Final sorted bids:")
        print_json(sortedBids)

        # TODO: What if the list is empty?
        winning_bids.append(sortedBids[0])

    return winning_bids


def get_adjusted_value(bid: Bid, bidder_adjustments: Dict[str, float]):
    return bid.bid + (bid.bid * bidder_adjustments[bid.bidder])


def get_config() -> Config:
    with open(pathlib.Path(__file__).parent / './config.json') as config_file:
        config_json_str = config_file.read()

    # TODO: Deserialize JSON into objects

    return Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                  [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])


def getAuctions() -> Auction:
    json_str = sys.stdin.read()

    # TODO: Deserialize JSON into objects

    return [Auction("houseofcheese.com",
                    ["banner", "sidebar"],
                    [Bid("AUCT", "banner", 35),
                     Bid("BIDD", "sidebar", 60),
                     Bid("AUCT", "sidebar", 55)])]


if __name__ == '__main__':
    main()
