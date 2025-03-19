


class Open_Trade:
    #für den fall, dass mehree opening trades gemacht werden, immer "openAvgPrice" nehmen für PNL rechnung
    def __init__(self, open_type, timestamp, price, leverage, volume, fees, margin, tp, sl):

        self.openType = open_type  # Isolated (1) oder cross order (2)
        self.timestamp = timestamp  # Timestamp eröffnung (in datum convertieren?)
        self.price = price
        self.leverage = leverage
        self.volume = volume
        self.fees = fees  # fees divided by amount of closing trades per position
        self.margin = margin # margin used for trade, e.g. buy 200€ of ETH --> 200 margin
        self.riskreward = None



        if(tp is not None and sl is not None):
            if(sl != price):
                self.riskreward = abs(tp-price) / abs(sl-price)
            else:
                self.riskreward = abs(tp - price) / price


