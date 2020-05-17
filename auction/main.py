#!usr/bin/env python3
import sys
import json
import pathlib
from typing import List, Dict

from . import json_encoder
from .auction import AuctionHelper, Auction, Bid
from .config import Config, Bidder, Site


def main():
    config = get_config()
    auctions = get_auctions()

    auction_helper = AuctionHelper(config)

    winning_bids: List[Bid] = []

    for auction in auctions:
        winning_bids.append(auction_helper.get_winning_bids(auction))

    print_json(winning_bids)


def print_json(data):
    """Prints JSON using the default encoder.

    Parameters:
    argument1 (int): Description of arg1

    """
    print(json.dumps(data, indent=4, cls=json_encoder.DefaultEncoder))


def get_config() -> Config:
    with open(pathlib.Path(__file__).parent / './config.json') as config_file:
        config_json_str = config_file.read()

    # TODO: Deserialize JSON into objects

    return Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                  [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])


def get_auctions() -> Auction:
    json_str = sys.stdin.read()

    # TODO: Deserialize JSON into objects

    return [Auction("houseofcheese.com",
                    ["banner", "sidebar"],
                    [Bid("AUCT", "banner", 35),
                     Bid("BIDD", "sidebar", 60),
                     Bid("AUCT", "sidebar", 55)])]


if __name__ == '__main__':
    main()
