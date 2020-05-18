#!usr/bin/env python3
import sys
import json
import pathlib
from typing import List

from . import json_encoder
from .auction import AuctionHelper, Auction, Bid
from .config import Config, Bidder, Site
from .json_decoder import auction_decoder, config_decoder


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

    :param data: Data to serialize and print.
    """
    print(json.dumps(data, indent=4, cls=json_encoder.DefaultEncoder))


def get_config() -> Config:
    """Gets the Config data from the local config file."""
    with open(pathlib.Path(__file__).parent / 'config.json') as config_file:
        config_json = config_file.read()

    return json.loads(config_json, object_hook=config_decoder)


def get_auctions() -> List[Auction]:
    """Gets the Auction data from standard in."""
    auction_json = sys.stdin.read()

    return json.loads(auction_json, object_hook=auction_decoder)


if __name__ == '__main__':
    main()
