import mysql.connector
from collections import defaultdict
from datetime import datetime, timedelta
import time
import json


from trade_group import Trade_Group
from close_trade import Close_Trade
from open_trade import Open_Trade
from user import User



def get_timestamps(self):
    for tr in self.trade_list:
        # print(datetime.datetime.fromtimestamp(tr.timestamp / 1000.0, tz=datetime.timezone.utc))
        print(str(tr.positionId) + "   " + str(datetime.fromtimestamp(tr.timestamp / 1000.0, )) + "    " + str(
            tr.category) + "   Liquidation Price: " + str(tr.liqprice))


def risk_vs_accountsize(self):
    for trade in self.trade_list:
        risk = trade.trade_risk()
        if (risk == None):
            continue
        pair = trade.pair.split("_")[1]
        entry = self.mexc_accountsize[pair]
        size = entry["equity"]
        print("RISK:  " + str(round(risk, 4)) + "    result: " + str(round(risk / size, 4)) + "    Time: " + str(
            str(datetime.fromtimestamp(trade.timestamp / 1000.0, ))))


def get_connection():
    return mysql.connector.connect(
    host="localhost",         # oder die IP-Adresse deines MySQL-Servers
    user="root",
    password="root",
    database="pa_db"
)
def new_risk_vs_accountsize(userID):
    conn = get_connection()
    trade_cursor = conn.cursor()
    asset_cursor = conn.cursor()

    asset_cursor.execute("""
    SELECT 
    """)

    trade_cursor.execute("""
    SELECT risk,pair
    FROM trade_group
    WHERE risk != NULL
    """)
    result = trade_cursor.fetchall()

    for pair in result:
        pass





def get_pnls(self):
    for trade in self.trade_list:
        print(trade.pnl)


def get_winrate(self):  # Hier trades pro positionId
    won = 0
    for tr in self.trade_list:
        Trade_Group.set_pnl(tr)
        if tr.outcome == 1:
            won += 1
    if (won != 0):
        self.winrate = (won / len(self.trade_list)) * 100
    else:
        self.winrate = 0


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
        # print(str(trade.outcome) + "    ||     " + str(trade.pnl) + "     ||        " + str(trade.total_margin))
        print(trade.outcome)


def get_rr_ratios(self):
    for index, trade in enumerate(self.trade_list):
        if trade.risk_reward != None:
            print("TP: " + str(trade.open_trades[0].tp) + "  |  Price: "
                  + str(trade.open_trades[0].price) + "  |  SL: " + str(
                trade.open_trades[0].sl) + "  |  RR-Ratio: " + str(round(trade.risk_reward, 4)))
            # for open in trade.open_trades:
            # print(open.riskreward)
            # print(str(trade.risk_reward))
            # print(f"Index: {index}, Trade: {trade}")


def calc_profitfactor_month(self):
    # get all trades within last 30 days
    thirty_days_ago_ms = round(time.time() * 1000) - (30 * 24 * 60 * 60 * 1000)
    lastmonth_list = []
    for trade in self.trade_list:
        if (trade.timestamp > thirty_days_ago_ms):
            lastmonth_list.append(trade)
    # get total wins and losses
    total_won = 0
    total_lost = 0
    for trade in lastmonth_list:
        # print(trade.pnl)
        if (trade.pnl >= 0):
            total_won += trade.pnl
        else:
            total_lost += trade.pnl

    print(total_lost)
    print(total_won)
    # return profit/loss
    factor = abs(total_won / total_lost)
    if (total_won < total_lost):
        return -1 * factor
    else:
        return factor


def positionsize_vs_pnl(self):
    avg = 0
    counter = 0
    wins = []
    losses = []
    for trade in self.trade_list:
        counter += 1
        if (len(trade.open_trades) != 0):
            current = trade.ps_v_pnl()
            if (current >= 0):
                wins.append(current)
            else:
                losses.append(current)
            print(str(round(current, 4)) + "   |   " + str(counter))
            avg += current
    avg_win = 0
    avg_loss = 0

    for x in wins:
        avg_win += x
    for x in losses:
        avg_loss += x

    avg_win = avg_win / len(self.trade_list)
    avg_loss = avg_loss / len(self.trade_list)
    print("average win: " + str(round(avg_win, 4)))
    print("average loss: " + str(round(avg_loss, 4)))
    print("average: " + str(round(avg / len(self.trade_list), 4)))


def trade_frequency_by_day(self):
    trade_by_date = defaultdict(list)

    # Group trades by date
    for trade in self.trade_list:
        trade_date = datetime.fromtimestamp(trade.timestamp / 1000).strftime('%d/%m/%Y')
        trade_by_date[trade_date].append(trade)

    # Sort dates descending by converting string back to datetime
    sorted_dates = sorted(trade_by_date.keys(), key=lambda d: datetime.strptime(d, '%d/%m/%Y'), reverse=True)

    for date in sorted_dates:
        trades = trade_by_date[date]
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
        print(str(tr.positionId) + "   " + str(datetime.fromtimestamp(tr.timestamp / 1000.0, ))
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
    for trade in self.trade_list:
        trade.check_liquidation()