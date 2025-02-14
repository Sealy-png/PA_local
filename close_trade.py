


class Close_Trade:

    def __init__(self, price, volume, timestamp, fees, profit):
        self.price = price
        self.volume = volume
        self.timestamp = timestamp
        self.fees = fees
        self.raw_profit = profit  # profit given by api does not include fees.
        self.profit = self.raw_profit - self.fees


    def get_price(self):
        return self.price

    def get_volume(self):
        return self.volume