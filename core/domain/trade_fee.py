import math


class BaseTradeFeePolicy:
    PROFIT_MARGIN_RATE = 0.005

    def calculate_buy_fee(self, price, quantity, **kwargs):
        return self._notional(price, quantity) * self._buy_fee_rate()

    def calculate_sell_fee(self, price, quantity, **kwargs):
        return self._notional(price, quantity) * self._sell_fee_rate()

    def calculate_sell_tax(self, price, quantity, **kwargs):
        return 0.0

    def calculate_buy_total(self, price, quantity, **kwargs):
        notional = self._notional(price, quantity)
        return notional + self.calculate_buy_fee(price, quantity, **kwargs)

    def calculate_sell_proceeds(self, price, quantity, **kwargs):
        notional = self._notional(price, quantity)
        return (
            notional
            - self.calculate_sell_fee(price, quantity, **kwargs)
            - self.calculate_sell_tax(price, quantity, **kwargs)
        )

    def calculate_round_trip_cost(self, buy_price, quantity, sell_price=None, **kwargs):
        sell_price = buy_price if sell_price is None else sell_price
        return self.calculate_buy_total(
            buy_price, quantity, **kwargs
        ) - self.calculate_sell_proceeds(sell_price, quantity, **kwargs)

    def max_buy_quantity(self, price, available_cash, **kwargs):
        price = float(price)
        cash = float(available_cash)
        if price <= 0 or cash <= 0:
            return 0

        low = 0
        high = max(int(cash / price), 0)
        while low < high:
            mid = (low + high + 1) // 2
            if self.calculate_buy_total(price, mid, **kwargs) <= cash:
                low = mid
            else:
                high = mid - 1
        return low

    def min_sell_quantity_for_target_net(self, price, target_amount, **kwargs):
        price = float(price)
        target_amount = float(target_amount)
        if price <= 0 or target_amount <= 0:
            return 0

        low = 1
        high = 1
        while self.calculate_sell_proceeds(price, high, **kwargs) < target_amount:
            high *= 2

        while low < high:
            mid = (low + high) // 2
            if self.calculate_sell_proceeds(price, mid, **kwargs) >= target_amount:
                high = mid
            else:
                low = mid + 1
        return low

    def break_even_sell_price(self, avg_buy_price, quantity, **kwargs):
        quantity = max(int(quantity), 1)
        avg_buy_price = float(avg_buy_price)
        if avg_buy_price <= 0:
            return 0.0

        target = self.calculate_target_sell_proceeds(avg_buy_price, quantity, **kwargs)
        low = 0.0
        high = max(avg_buy_price, self._price_step())
        while self.calculate_sell_proceeds(high, quantity, **kwargs) < target:
            high *= 2

        for _ in range(60):
            mid = (low + high) / 2
            if self.calculate_sell_proceeds(mid, quantity, **kwargs) >= target:
                high = mid
            else:
                low = mid
        return self._round_up_price(high)

    def calculate_target_sell_proceeds(self, avg_buy_price, quantity, **kwargs):
        return self.calculate_buy_total(avg_buy_price, quantity, **kwargs) * (
            1.0 + self.PROFIT_MARGIN_RATE
        )

    def _notional(self, price, quantity):
        return float(price) * int(quantity)

    def _buy_fee_rate(self):
        raise NotImplementedError

    def _sell_fee_rate(self):
        raise NotImplementedError

    def _price_step(self):
        raise NotImplementedError

    def _round_up_price(self, price):
        step = self._price_step()
        rounded = math.ceil(float(price) / step - 1e-12) * step
        if step < 1:
            return round(rounded, 2)
        return float(int(rounded))


class KoreaTradeFeePolicy(BaseTradeFeePolicy):
    FEE_RATE = 0.00015
    SELL_TAX_RATE = 0.002
    TAX_EXEMPT_MARKETS = {"ETF", "ETN"}

    def calculate_sell_tax(self, price, quantity, market_name=None, **kwargs):
        market_name = market_name or kwargs.get("market_name")
        if market_name in self.TAX_EXEMPT_MARKETS:
            return 0.0
        return self._notional(price, quantity) * self.SELL_TAX_RATE

    def _buy_fee_rate(self):
        return self.FEE_RATE

    def _sell_fee_rate(self):
        return self.FEE_RATE

    def _price_step(self):
        return 1.0


class USTradeFeePolicy(BaseTradeFeePolicy):
    FEE_RATE = 0.0025
    SEC_FEE_RATE = 20.60 / 1_000_000
    TAF_PER_SHARE = 0.000195
    TAF_CAP = 9.79

    def calculate_sell_tax(self, price, quantity, **kwargs):
        notional = self._notional(price, quantity)
        return (notional * self.SEC_FEE_RATE) + min(
            int(quantity) * self.TAF_PER_SHARE,
            self.TAF_CAP,
        )

    def _buy_fee_rate(self):
        return self.FEE_RATE

    def _sell_fee_rate(self):
        return self.FEE_RATE

    def _price_step(self):
        return 0.01
