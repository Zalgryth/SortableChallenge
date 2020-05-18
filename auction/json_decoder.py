from .auction import AuctionHelper, Auction, Bid
from .config import Config, Bidder, Site


def config_decoder(data):
    """A JSON Decoder to map a JSON object to a Config object.

    This can be passed in for the object_hook parameter in json.loads.
    """
    # There doesn't appear to be any easy way to convert JSON to Python objects...
    # This will have to do for now.
    if 'name' in data and 'bidders' in data and 'floor' in data:
        return Site(data['name'], data['bidders'], data['floor'])
    if 'name' in data and 'adjustment' in data:
        return Bidder(data['name'], data['adjustment'])
    return Config(data['sites'], data['bidders'])


def auction_decoder(data):
    """A JSON Decoder to map a JSON object to an Auction object.

    This can be passed in for the object_hook parameter in json.loads.
    """
    # There doesn't appear to be any easy way to convert JSON to Python objects...
    # This will have to do for now.
    if 'bidder' in data and 'unit' in data and 'bid' in data:
        return Bid(data['bidder'], data['unit'], data['bid'])
    return Auction(data['site'], data['units'], data['bids'])
