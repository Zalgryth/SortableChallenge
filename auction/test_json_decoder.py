import json
import unittest

from .auction import AuctionHelper, Auction, Bid
from .config import Config, Bidder, Site
from .json_decoder import auction_decoder, config_decoder


class TestJsonDecoder(unittest.TestCase):

    def test_auction_decoder_works(self):
        auction_json = """
[
    {
        "site": "houseofcheese.com",
        "units": [
            "banner",
            "sidebar"
        ],
        "bids": [
            {
                "bidder": "AUCT",
                "unit": "banner",
                "bid": 35
            },
            {
                "bidder": "BIDD",
                "unit": "sidebar",
                "bid": 60
            },
            {
                "bidder": "AUCT",
                "unit": "sidebar",
                "bid": 55
            }
        ]
    }
]
        """

        expected_auctions = [Auction("houseofcheese.com",
                                     ["banner", "sidebar"],
                                     [Bid("AUCT", "banner", 35),
                                      Bid("BIDD", "sidebar", 60),
                                      Bid("AUCT", "sidebar", 55)])]

        actual_auctions = json.loads(auction_json, object_hook=auction_decoder)

        self.assertListEqual(expected_auctions, actual_auctions)

    def test_config_decoder_works(self):
        config_json = """
{
    "sites": [
        {
            "name": "houseofcheese.com",
            "bidders": ["AUCT", "BIDD"],
            "floor": 32
        }
    ],
    "bidders": [
        {
            "name": "AUCT",
            "adjustment": -0.0625
        },
        {
            "name": "BIDD",
            "adjustment": 0
        }
    ]
}
        """

        expected_config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                                 [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        actual_config = json.loads(config_json, object_hook=config_decoder)

        self.assertEqual(expected_config, actual_config)
