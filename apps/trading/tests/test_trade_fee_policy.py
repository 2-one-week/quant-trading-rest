import unittest

from core.domain import KoreaTradeFeePolicy, USTradeFeePolicy


class TradeFeePolicyTest(unittest.TestCase):
    def setUp(self):
        self.korea_policy = KoreaTradeFeePolicy()
        self.us_policy = USTradeFeePolicy()

    def test_korea_stock_round_trip_uses_sell_tax(self):
        buy_total = self.korea_policy.required_buy_cash(10000, 10)
        sell_proceeds = self.korea_policy.calculate_sell_proceeds(10000, 10)

        self.assertAlmostEqual(buy_total, 100015.0)
        self.assertAlmostEqual(sell_proceeds, 99785.0)
        self.assertAlmostEqual(
            self.korea_policy.calculate_round_trip_cost(10000, 10),
            230.0,
        )

    def test_korea_etf_sell_tax_is_exempt(self):
        sell_tax = self.korea_policy.calculate_sell_tax(110000, 5, market_name="ETF")
        self.assertEqual(sell_tax, 0.0)

    def test_us_sell_cost_includes_sec_fee_and_taf(self):
        sell_tax = self.us_policy.calculate_sell_tax(100.0, 10)
        self.assertAlmostEqual(sell_tax, 0.02255, places=6)

    def test_min_sell_price_for_profit_uses_margin_and_sell_costs(self):
        break_even = self.us_policy.min_sell_price_for_profit(100.0, 10)
        target_sell_proceeds = self.us_policy.target_sell_proceeds(100.0, 10)

        self.assertGreaterEqual(
            self.us_policy.calculate_sell_proceeds(break_even, 10),
            target_sell_proceeds,
        )
        self.assertLess(
            self.us_policy.calculate_sell_proceeds(round(break_even - 0.01, 2), 10),
            target_sell_proceeds,
        )


if __name__ == "__main__":
    unittest.main()
