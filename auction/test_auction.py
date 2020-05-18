import unittest

from .auction import AuctionHelper, Auction, Bid
from .config import Config, Bidder, Site


class TestAuctionHelper(unittest.TestCase):

    def test_winning_bid_passes_provided_test_sample_works(self):
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

    def test_winning_bid_no_bidder_config_ignores_bid(self):
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

    def test_winning_bid_ignores_bid_not_in_auction_units(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 35),
                           Bid("BIDD", "sidebar", 55),
                           Bid("AUCT", "notinauction", 60000)])

        auction_helper = AuctionHelper(config)

        # There should be no winning bids for the non-existant unit.
        expected_winning_bids = [Bid("AUCT", "banner", 35),
                                 Bid("BIDD", "sidebar", 55)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_ignores_negative_bid(self):
        # Negative floor to ensure that negative bids are ignored not just because
        # they go below the floor, but because they're below 0.
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], -50)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", -5),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # No banner winner since the only bid was negative.
        expected_winning_bids = [Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_negative_floor_works_with_positive_bids(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], -50)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 5),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # Despite the negative floor, bids should still work.
        expected_winning_bids = [Bid("AUCT", "banner", 5),
                                 Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_duplicate_auction_units_performs_multiple_auctions(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar", "sidebar"],
                          [Bid("AUCT", "banner", 35),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # There should be one winning bid per unit request, even if duplicate.
        expected_winning_bids = [Bid("AUCT", "banner", 35),
                                 Bid("BIDD", "sidebar", 60),
                                 Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertEqual(len(expected_winning_bids), len(actual_winning_bids))
        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_site_not_in_config_no_winners(self):
        config = Config([Site("houseofnotcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 35),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # There should not be any winning bids - invalid site config!
        # Because of a lack of valid site, there's no way to determine
        # allowed bidders or bid floor. Rather than blow up, just return
        # no bids.
        expected_winning_bids = []
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_positive_adjustment_works(self):
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", 0), Bidder("BIDD", 0.5)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 35),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 89)])

        auction_helper = AuctionHelper(config)

        # BIDD should adjust up to 90 and win.
        expected_winning_bids = [Bid("AUCT", "banner", 35),
                                 Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_duplicate_site_configs_doesnt_fail(self):
        # Duplicate site configs is bad data and shouldn't happen,
        # but if it does, we shouldn't blow up to still allow for
        # auctions to occur. Simply use one of the site configs.
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32),
                         Site("houseofcheese.com", ["AUCT", "BIDD"], 28)],
                        [Bidder("AUCT", -0.0625), Bidder("BIDD", 0)])

        # Make the banner less than both of the configs.
        # We shouldn't make any guarantees about which of the configs
        # we're using. All that matters is that we pulled from one of them
        # and that the bid that is lower than both configs will get rejected
        # every time.
        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 25),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 55)])

        auction_helper = AuctionHelper(config)

        # The banner one gets rejected for being below either of the configured floors.
        expected_winning_bids = [Bid("BIDD", "sidebar", 60)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)

    def test_winning_bid_duplicate_bidder_configs_doesnt_fail(self):
        # Duplicate bidder configs is bad data and shouldn't happen,
        # but if it does, we shouldn't blow up to still allow for
        # auctions to occur. Simply use one of the bidder configs.
        config = Config([Site("houseofcheese.com", ["AUCT", "BIDD"], 32)],
                        [Bidder("AUCT", -0.0625), Bidder("AUCT", -0.07), Bidder("BIDD", 0)])

        auction = Auction("houseofcheese.com",
                          ["banner", "sidebar"],
                          [Bid("AUCT", "banner", 40),
                           Bid("BIDD", "sidebar", 60),
                           Bid("AUCT", "sidebar", 90)])

        auction_helper = AuctionHelper(config)

        # Either of the adjustments still cause it to win, so just make sure
        # it works.
        expected_winning_bids = [Bid("AUCT", "banner", 40),
                                 Bid("AUCT", "sidebar", 90)]
        actual_winning_bids = auction_helper.get_winning_bids(auction)

        self.assertListEqual(expected_winning_bids, actual_winning_bids)


if __name__ == '__main__':
    unittest.main()
