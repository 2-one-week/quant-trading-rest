from abc import ABC, abstractmethod

class InvestmentWrapper(ABC):
    @abstractmethod
    def connect(self, mode):
        pass

    @abstractmethod
    def get_last_prices(self, symbol, tick, input_desc):
        pass

    @abstractmethod
    def update_by_minute(self, symbol):
        pass

    @abstractmethod
    def get_current_price(self, symbol):
        pass

    @abstractmethod
    def check_and_update_stock_info(self, symbol, info):
        pass
    
    @abstractmethod
    def buy_stock_by_market_price(self, symbol, quantity):
        pass
    
    @abstractmethod
    def sell_stock_by_market_price(self, symbol, quantity):
        pass

    @abstractmethod
    def required_buy_cash(self, symbol, price, quantity):
        pass

    @abstractmethod
    def min_sell_price_for_profit(self, symbol, avg_buy_price, quantity):
        pass

    @abstractmethod
    def max_affordable_buy_quantity(self, symbol, price, available_cash):
        pass

    @abstractmethod
    def required_sell_quantity_for_cash(self, symbol, price, target_amount):
        pass
