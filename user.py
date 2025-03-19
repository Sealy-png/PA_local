from audioop import avgpp
from collections import defaultdict
from datetime import datetime, timedelta
import time
import json
import os

import mexc_api as mexc
from close_trade import Close_Trade
from open_trade import Open_Trade
from trade_group import Trade_Group


# api_key = "mx0vglIoQqFLx6wZet", api_secret = "6d73718cedc3423e9fb1217204b5d38e"
class User:
    api_key = ""
    api_secret = ""

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.trade_list = []
        self.winrate = 0
        self.be_point = 0  # percentage of margin where trade becomes break_even

    def set_be_point(self, point):  #Should be created during intitializationn for usage, only to save dev time. Given in whole numbers:  1 = 1%
        self.be_point = point/100

    def get_timestamps(self):
        for tr in self.trade_list:
            # print(datetime.datetime.fromtimestamp(tr.timestamp / 1000.0, tz=datetime.timezone.utc))
            print(str(tr.positionId) + "   " + str(datetime.fromtimestamp(tr.timestamp / 1000.0,
                                                                                   )) + "    " + str(tr.category))


    def get_pnls(self):
        for trade in self.trade_list:
            print(trade.pnl)



    def get_winrate(self): # Hier trades pro positionId
        won = 0
        for tr in self.trade_list:
            Trade_Group.set_pnl(tr)
            if tr.outcome == 1:
                won += 1
        if(won != 0):
            self.winrate = (won / len(self.trade_list)) * 100
        else:
            self.winrate= 0

    def get_traded_assets(self):
        assets = {}
        for trade in self.trade_list:
            pair = trade.pair
            if pair in assets:
                assets[pair] += 1
            else:
                assets[pair] = 1
        print(assets)

    def long_short_ratio(self):
        longs = 0
        shorts = 0
        for trade in self.trade_list:
            if trade.side == 2:
                shorts += 1
            if trade.side == 4:
                longs += 1

        print("total trades: " + str(len(self.trade_list)))
        print("long / short ratio: " + str(longs) + " / " + str(shorts))

    def net_profit(self):
        net = 0
        for trade in self.trade_list:
            net += trade.pnl

        print(net)



    def get_outcomes(self):
        for trade in self.trade_list:
            #print(str(trade.outcome) + "    ||     " + str(trade.pnl) + "     ||        " + str(trade.total_margin))
            print(trade.outcome)


    def calc_profitfactor_month(self):
        #get all trades within last 30 days
        thirty_days_ago_ms = round(time.time() * 1000) - (30 * 24 * 60 * 60 * 1000)
        lastmonth_list = []
        for trade in self.trade_list:
            if(trade.timestamp > thirty_days_ago_ms):
                lastmonth_list.append(trade)
        # get total wins and losses
        total_won = 0
        total_lost = 0
        for trade in lastmonth_list:
            if(trade.pnl >= 0):
                total_won += trade.pnl
            else:
                total_lost+= trade.pnl
        # return profit/loss
        return total_won/total_lost

    def positionsize_vs_pnl(self):
        avg = 0
        for trade in self.trade_list:
            current = trade.ps_v_pnl()
            print(current)
            avg += current
        print("avergae: "+ str(avg/len(self.trade_list)))


    def trade_frequency_by_day(self):
        trade_by_date = defaultdict(list)

        # Group trades by date
        for trade in self.trade_list:
            trade_date = datetime.fromtimestamp(trade.timestamp/1000).strftime('%d/%m/%Y')
            trade_by_date[trade_date].append(trade)

        for date, trades in sorted(trade_by_date.items()):
            print(f"{date}:", end=" ")
            trade_details = [f"positionId = {trade.positionId}, pnl = {trade.pnl}" for trade in trades]
            print("; ".join(trade_details))

    def trade_frequency_by_week(self):
        trade_by_week = defaultdict(list)

        for trade in self.trade_list:
            trade_date = datetime.fromtimestamp(trade.timestamp / 1000)
            iso_year, iso_week, _ = trade_date.isocalendar()  # ISO year and week number

            # Find the Monday of the ISO week in the correct year
            start_of_week = datetime.strptime(f'{iso_year}-W{iso_week}-1', "%G-W%V-%u")
            end_of_week = start_of_week + timedelta(days=6)

            week_label = f"KW {iso_week} {iso_year}, {start_of_week.strftime('%d.%m.%y')} - {end_of_week.strftime('%d.%m.%y')}"
            trade_by_week[(iso_year, iso_week)].append((week_label, trade))
        # Sort by year and week number chronologically
        sorted_weeks = sorted(trade_by_week.items())
        for (_, trades) in sorted_weeks:
            week_label = trades[0][0]  # Extract week label from the first entry
            print(f"{week_label} ({len(trades)} trades):", end=" ")
            trade_details = [f"positionId = {trade.positionId}, pnl = {trade.pnl}" for _, trade in trades]
            print("; ".join(trade_details))


    def get_longest_streak(self):
        current_streak = 0
        longest_streak = 0
        current_streak_list = []
        longest_streak_list = []

        for trade in self.trade_list:
            if trade.outcome == 1:
                current_streak += 1
                current_streak_list.append(trade)
            else:
                if current_streak > longest_streak:
                    longest_streak = current_streak
                    longest_streak_list = current_streak_list[:]

                current_streak = 0
                current_streak_list = []

        if current_streak > longest_streak:
            longest_streak = current_streak
            longest_streak_list = current_streak_list[:]

        for tr in longest_streak_list:
            print(str(tr.positionId) + "   " + str(datetime.fromtimestamp(tr.timestamp / 1000.0,))
                  + "    " + str(tr.outcome))
        # return longest_streak, longest_streak_list

    def long_short_winrate(self):
        longamount = 0
        longrate = 0
        shortamount = 0
        shortrate = 0
        for tr in self.trade_list:
            Trade_Group.post_init(tr)
            if tr.side == 2:
                shortamount += 1
                if tr.pnl > 0:
                    shortrate += 1
            if tr.side == 4:
                longamount += 1
                if tr.pnl > 0:
                    longrate += 1
        shortwinrate = (shortrate / shortamount) * 100
        longwinrate = (longrate / longamount) * 100
        print(" Winrate shorts: " + str(shortwinrate) + " || Winrate longs: " + str(longwinrate))

    def get_tp_hitrate(self):
        hits = 0
        for trade in self.trade_list:
            if trade.tp_hit:
                hits += 1
        print("TP hitrate: " + str(round((hits / len(self.trade_list)) * 100, 2)) + "%")

    def get_sl_hitrate(self):
        hits = 0
        for trade in self.trade_list:
            if trade.sl_hit:
                hits += 1
        print("SL hitrate: " + str(round((hits / len(self.trade_list)) * 100, 2)) + "%")

    def avg_win_loss(self):
        wins = 0
        winval = 0
        losses = 0
        lossval = 0
        for tr in self.trade_list:
            Trade_Group.post_init(tr)
            if tr.pnl > 0:
                wins += 1
                winval += tr.pnl
            elif tr.pnl < 0:
                losses += 1
                lossval += tr.pnl

        avgwin = winval / wins
        avgloss = lossval / losses

        print("Average amount won: " + str(avgwin) + " || Average amount lost: " + str(avgloss))

    def get_liquidations(self):
        liquidations = []
        for trade in self.trade_list:
            if trade.category == 2:
                liquidations.append(trade)
        return len(liquidations) / len(self.trade_list) * 100


















    def get_trades_mexc(self):
        # history = mexc.get_history_orders(self.api_key, self.api_secret,start_time=	1730415600000, end_time=1737591241739,page_size='100')['data']
        end = time.time_ns() // 1000000
        start = time.time_ns() // 1000000 - 7776000000
        history = mexc.get_history_orders(self.api_key, self.api_secret, start_time=start, end_time=end, page_size='100')['data']
        grouped_trades = self.group_trades_by_key(history)
        self.create_trade_groups(grouped_trades)

    @staticmethod
    def group_trades_by_key(trades):
        """
        Create dictionary with positionId as key, each having a list of trades associated with the ID

        :return: Dictionary with grouped trades
        """
        grouped = {}
        for trade in trades:
            value = trade['positionId']
            if value not in grouped:
                grouped[value] = []
            grouped[value].append(trade)
        print(len(grouped))
        return grouped



    def create_trade_groups(self, trades):
        """
        Iterates over dictionary created in /group_trades_by_key/, checks each position ID and creates a trade for each closing action

        :param trades:
        :return: none
        """
        print(len(trades))
        for position_id, trades in trades.items():


            # Separate buy and sell trades
            open_trades = [trade for trade in trades if trade['state'] == 3 and (
                    trade['side'] == 1 or trade['side'] == 3)]  # 1 = open_trade long, 3 = open_trade short
            close_trades = [trade for trade in trades if trade['state'] == 3 and (
                    trade['side'] == 2 or trade['side'] == 4)]  # 2 = close_trade short, 4 = close_trade long

            if (len(close_trades) == 0):
                continue

            # If multiple sell trades exist, divide fees equally among each sell trade
            buy_fees = 0
            for trade in open_trades:
                buy_fees += trade['makerFee']
                buy_fees += trade['takerFee']
            buy_fees: int = buy_fees

            # Create a TradeGroup for each sell trade
            template = close_trades[0]
            trade = Trade_Group(positionId=position_id, side=template['side'], pair=template['symbol'],
                                category=template['category'], be_point=self.be_point)


            # Add all buy trades to the trade group
            for open_trade in open_trades:
                trade.add_open_trade(Open_Trade(
                    open_type=open_trade['openType'],
                    price=open_trade['price'],
                    volume=open_trade['dealVol'],
                    leverage=open_trade['leverage'],
                    timestamp=open_trade['createTime'],
                    margin=open_trade['usedMargin'],
                    tp=open_trade.get('takeProfitPrice',None),
                    sl=open_trade.get('stopLossPrice', None),
                    fees = buy_fees
                    ))

                # Set the sell trade for the trade group
            for close_trade in close_trades:
                sell_fees = close_trade.get('makerFee', None) + close_trade.get('takerFee', None)
                trade.add_close_trade(Close_Trade(
                    price=close_trade['dealAvgPrice'],
                    volume=close_trade['dealVol'],
                    timestamp=close_trade['createTime'],
                    profit=close_trade['profit'],
                    fees=sell_fees
                    ))


            for close_trade in close_trades:
                if 'externalOid' in close_trade and "STOP_LOSS" in close_trade['externalOid']:
                    trade.set_slhit()
                if 'externalOid' in close_trade and "TAKE_PROFIT" in close_trade['externalOid']:
                    trade.set_tphit()
                # Append the trade group to the trades list

            self.trade_list.append(trade)
            Trade_Group.post_init(trade)

    @staticmethod
    def text_group_trades_by_key():
        """
        Create dictionary with positionId as key, each having a list of trades associated with the ID

        :return: Dictionary with grouped trades
        """
        file_path = 'C:\\Users\\Ammar\\PycharmProjects\\PA_local\\output.txt'
        with open(file_path, 'r') as file:
            data = json.load(file)
        grouped = {}
        trades = data['data']
        #print(json.dumps(trades))

        for trade in trades:
            value = trade['positionId']
            if value not in grouped:
                grouped[value] = []
            grouped[value].append(trade)
        print(len(grouped))
        return grouped

    def text_create_trade_groups(self, trades):
        """
        Iterates over dictionary created in /group_trades_by_key/, checks each position ID and creates a trade for each closing action

        :param trades:
        :return: none
        """
        print(len(trades))
        for position_id, trades in trades.items():


            # Separate buy and sell trades
            open_trades = [trade for trade in trades if trade['state'] == 3 and (
                    trade['side'] == 1 or trade['side'] == 3)]  # 1 = open_trade long, 3 = open_trade short
            close_trades = [trade for trade in trades if trade['state'] == 3 and (
                    trade['side'] == 2 or trade['side'] == 4)]  # 2 = close_trade short, 4 = close_trade long

            if (len(close_trades) == 0):
                continue

            # If multiple sell trades exist, divide fees equally among each sell trade
            buy_fees = 0
            for trade in open_trades:
                buy_fees += trade['makerFee']
                buy_fees += trade['takerFee']
            buy_fees: int = buy_fees

            # Create a TradeGroup for each sell trade
            template = close_trades[0]
            trade = Trade_Group(positionId=position_id, side=template['side'], pair=template['symbol'],
                                category=template['category'], be_point=self.be_point)


            # Add all buy trades to the trade group
            for open_trade in open_trades:
                trade.add_open_trade(Open_Trade(
                    open_type=open_trade['openType'],
                    price=open_trade['price'],
                    volume=open_trade['dealVol'],
                    leverage=open_trade['leverage'],
                    timestamp=open_trade['createTime'],
                    margin=open_trade['usedMargin'],
                    tp=open_trade.get('takeProfitPrice',None),
                    sl=open_trade.get('stopLossPrice', None),
                    fees = buy_fees
                    ))

                # Set the sell trade for the trade group
            for close_trade in close_trades:
                sell_fees = close_trade.get('makerFee', None) + close_trade.get('takerFee', None)
                trade.add_close_trade(Close_Trade(
                    price=close_trade['dealAvgPrice'],
                    volume=close_trade['dealVol'],
                    timestamp=close_trade['createTime'],
                    profit=close_trade['profit'],
                    fees=sell_fees
                    ))


            for close_trade in close_trades:
                if 'externalOid' in close_trade and "STOP_LOSS" in close_trade['externalOid']:
                    trade.set_slhit()
                if 'externalOid' in close_trade and "TAKE_PROFIT" in close_trade['externalOid']:
                    trade.set_tphit()
                # Append the trade group to the trades list

            self.trade_list.append(trade)
            Trade_Group.post_init(trade)