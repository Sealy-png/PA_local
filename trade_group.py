class Trade_Group:

    def __init__(self, positionId, side, pair, category, be_point):  # outcomepoint für BE rechnung
        self.positionId = positionId
        self.side = side  # 2 = short, 4 = long
        self.pair = pair   # Coin pair, e.g. BTCUSDT, ETH, etc.
        self.category = category  # 2 = liquidation?
        self.open_trades = []
        self.close_trades = []
        self.price = 0  # average of all open trade prices (relative to volume)
        self.pnl = 0  # aus API profit - alle makker/takerfees
        self.tp_hit = False
        self.sl_hit = False
        self.be_point = be_point
        self.outcome = 0  # -1 = loss, 0 = break evenn, 1 = profit
        self.fees = 0
        self.risk_reward = 0
        self.timestamp = None
        self.total_margin = 0
        self.liqprice = None
        self.risk = 0


    def post_init(self):
        """
        Call after initialization is finished(including open/close trades being set.
        Does all calculations that can't be done before all data is added, needs to be called once.

        :params: none
        :return:none
        """
        self.calc_open_price()
        self.set_fees()  # used in set_pnl
        self.set_pnl()   # used in set_outcome
        self.set_outcome() #sets margin
        self.find_highest_timestamp() # no dependencies
        self.set_rr_ratios()





    def set_rr_ratios(self):
        total_riskreward = 0
        total_weight = 0

        for trade in self.open_trades:
            if trade.riskreward is not None:
                weight = trade.margin / self.total_margin
                total_riskreward += weight * trade.riskreward
                total_weight += weight

        if total_weight > 0:
            self.risk_reward = total_riskreward / total_weight
        else:
            self.risk_reward = None  # oder 0, falls du einen Default willst

    def check_liquidation(self):
        for trade in self.close_trades:
            print("Liquidation Price: " + str(self.liqprice) + "   Actual Price: " + str(trade.price))
            if(trade.price == self.liqprice):
                print(self.positionId)

    def trade_risk(self):
        #Berechne StopLoss für risk rechnung
        avg_sl = 0
        count_sl = 0
        for trade in self.open_trades:
            if trade.sl != None:
                avg_sl += trade.sl
                count_sl += 1
        if(count_sl != 0):
            avg_sl = avg_sl/count_sl

            positionsize = self.calcpositionsize()
            debug = self.price
            risk = abs(self.price - avg_sl) * positionsize
            return risk
        else:
            return None




    def set_outcome(self):  # marge muss durch den be point gesetzt werden wenn trade erstellt wird, point kommt aus dem user
        """
        Was ist mein ansatz? be_point = 0.1% für beispiel
        wenn position 100% aufgelöst --> pnl > 0.01 * net margin

        :return:
        """
        profit = self.pnl
        test = self.be_point
        theo_be_point = 0
        self.get_margin()
        if(self.be_point != 0):
            theo_be_point = self.total_margin * self.be_point

        if(self.pnl > theo_be_point):
            self.outcome = 1
        elif (abs(profit)<abs(theo_be_point)):
            self.outcome = 0
        else:
            self.outcome = -1

    def get_margin(self):
        total_margin = 0
        for trade in self.open_trades:
            total_margin += trade.margin

        self.total_margin = total_margin


    def set_fees(self):
        total_fees = 0
        for trade in self.open_trades:
            total_fees += trade.fees

        # Needs fees to be set, otherwise value is wrong. Does not include funding fee
        for trade in self.close_trades:
            total_fees += trade.fees
        self.fees = total_fees

    def set_pnl(self):  # differenzieren zwischen long short
        for trade in self.close_trades:
            self.pnl += trade.raw_profit

        self.pnl -= self.fees


    def find_highest_timestamp(self):
        stamps = []
        for trade in self.close_trades:
            stamps.append(trade.timestamp)
        self.timestamp = max(stamps)

    def print_Trade(self):
        print(self.positionId)

    def add_open_trade(self, openTrade):
        self.open_trades.append(openTrade)

    def add_close_trade(self,closeTrade):
        self.close_trades.append(closeTrade)

    def calc_open_price(self):
        total_volume = sum(trade.volume for trade in self.open_trades)
        weighed_sum = sum(trade.price*trade.volume for trade in self.open_trades)

        if(total_volume == 0):
            self.price = 0

        self.price = weighed_sum/total_volume


    # prozentsatz vom pnl relativ zur positionsgröße
    def ps_v_pnl(self):
        size = self.calcpositionsize()
        if (len(self.open_trades) != 0):
            return self.pnl/size
        else:
            return None

    def calcpositionsize(self):
        size = 0

        for trade in self.open_trades:
            size += trade.margin * trade.leverage
        return size





    def set_tphit(self):
        self.tp_hit = True

    def set_slhit(self):
        self.sl_hit = True



