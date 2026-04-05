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
    def calculate_buy_total(self, symbol, price, quantity):
        pass

    @abstractmethod
    def calculate_break_even_sell_price(self, symbol, avg_buy_price, quantity):
        pass

    @abstractmethod
    def max_buy_quantity(self, symbol, price, available_cash):
        pass

    @abstractmethod
    def min_sell_quantity_for_target_net(self, symbol, price, target_amount):
        pass
