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

    :param data: Data to serialize and print.
    """
    print(json.dumps(data, indent=4, cls=json_encoder.DefaultEncoder))


def get_config() -> Config:
    """Gets the Config data from the local config file."""
    with open(pathlib.Path(__file__).parent / './config.json') as config_file:
        config_json = config_file.read()

    return json.loads(config_json, object_hook=config_decoder)


def get_auctions() -> Auction:
    """Gets the Auction data from standard in."""
    auction_json = sys.stdin.read()

    return json.loads(auction_json, object_hook=auction_decoder)


def config_decoder(data):
    """A JSON Decoder to map a JSON object to a Config object."""
    # There doesn't appear to be any easy way to convert JSON to Python objects...
    # This will have to do for now.
    if 'name' in data and 'bidders' in data and 'floor' in data:
        return Site(data['name'], data['bidders'], data['floor'])
    if 'name' in data and 'adjustment' in data:
        return Bidder(data['name'], data['adjustment'])
    return Config(data['sites'], data['bidders'])


def auction_decoder(data):
    """A JSON Decoder to map a JSON object to an Auction object."""
    # There doesn't appear to be any easy way to convert JSON to Python objects...
    # This will have to do for now.
    if 'bidder' in data and 'unit' in data and 'bid' in data:
        return Bid(data['bidder'], data['unit'], data['bid'])
    return Auction(data['site'], data['units'], data['bids'])


if __name__ == '__main__':
    main()
