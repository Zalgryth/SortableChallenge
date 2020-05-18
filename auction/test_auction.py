import unittest

from .auction import AuctionHelper, Auction, Bid
from .config import Config, Bidder, Site


class TestAuctionHelper(unittest.TestCase):

    def test_winning_bid_passes_provided_test_sample(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 35),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # These come from output.json in the challenge.
        expected_winning_bids = [Bid("AUCT", "banner", 35),
                                 Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_rejects_lower_than_floor_including_adjustments(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.5), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 50),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # No banner result because its adjusted value is below the site's floor.
        expected_winning_bids = [Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_ignores_unit_not_on_site(self):
        config = Config([Site("houseofcheese.com", ["AUCT"], 32)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 35),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # BIDD would win, but isn't on the site config, so AUCT wins it all.
        expected_winning_bids = [Bid("AUCT", "banner", 35),
                                 Bid("AUCT", "sidebar", 55)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_calculates_maximum_using_adjustments(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.25), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("BIDD", "sidebar", 76),
                           Bid("AUCT", "sidebar", 100)])

        auction_helper = AuctionHelper(config)

        # The AUCT bid gets reduced from 100 to 75 and loses to BIDD.
        expected_winning_bids = [Bid("BIDD", "sidebar", 76)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_no_bidder_config(self):
        # if there's no configuration for a bidder, but somehow it's in the site config and bid
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 3500),
                           Bid("BIDD", "sidebar", 55),
                           Bid("AUCT", "sidebar", 6000)])

        auction_helper = AuctionHelper(config)

        # AUCT would win here, but there's no config setup, so BIDD wins.
        expected_winning_bids = [Bid("BIDD", "sidebar", 55)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)


if __name__ == '__main__':
    unittest.main()
