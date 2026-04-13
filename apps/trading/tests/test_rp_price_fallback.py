import unittest
from types import SimpleNamespace

from core.domain import StockTick
from core.infra.kiwoom_wrapper import KiwoomWrapper


class _FakeKiwoomAPI:
    def __init__(self):
        self.last_order = None

    def get_hoga(self, symbol):
        return {"return_code": 1, "return_msg": "NO_PRICE"}

    def get_stock_price_info(self, symbol):
        return {
            "stk_cd": symbol,
            "cur_prc": "100500",
            "return_code": 0,
            "return_msg": "OK",
        }

    def send_order(self, symbol, quantity, buy, price):
        self.last_order = {
            "symbol": symbol,
            "quantity": quantity,
            "buy": buy,
            "price": price,
        }
        return {"return_code": 0, "return_msg": "OK", "price": price}


class RPPriceFallbackTest(unittest.TestCase):
    def setUp(self):
        self.stock_db = SimpleNamespace(
            price_db={"423160": {StockTick.MIN1: []}},
            name_table={"423160": "KODEX KOFR"},
            record_minute_price=lambda *args, **kwargs: None,
        )
        self.wrapper = KiwoomWrapper(stock_db=self.stock_db)
        self.wrapper.kiwoom = _FakeKiwoomAPI()
        self.wrapper.mock = False

    def test_sell_rp_uses_current_price_when_min1_cache_empty(self):
        executed = self.wrapper.sell_stock_by_market_price("423160", 2)

        self.assertEqual(executed, 2)
        self.assertEqual(self.wrapper.kiwoom.last_order["price"], 100500)


if __name__ == "__main__":
    unittest.main()
