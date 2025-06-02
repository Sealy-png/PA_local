import mysql.connector
from collections import defaultdict
from datetime import datetime, timedelta
import time
import json

from wasabi import table

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





def get_pnls(mistake =None, setup=None):
    columns = ["pnl"]
    trades = call_db(columns, "trade_group", mistake, setup)
    for trade in trades:
        print(trade["pnl"])


def get_winrate(mistake =None, setup=None):  # Hier trades pro positionId
    won = 0

    columns = ["outcome"]
    trades = call_db(columns, "trade_group", mistake, setup)
    for tr in trades:
        if tr["outcome"] == 1:
            won += 1

    winrate = 0
    if (won != 0):
        winrate = (won / len(trades)) * 100
    else:
        winrate = 0


def get_traded_assets(self):
    assets = {}
    for trade in self.trade_list:
        pair = trade.pair
        if pair in assets:
            assets[pair] += 1
        else:
            assets[pair] = 1
    print(assets)


def long_short_ratio(mistake =None, setup=None):
    longs = 0
    shorts = 0

    columns = ["side"]
    trades = call_db(columns, "trade_group", mistake, setup)

    for trade in trades:
        if trade["side"] == 2:
            shorts += 1
        if trade["side"] == 4:
            longs += 1

    print("total trades: " + str(len(trades)))
    print("long / short ratio: " + str(longs) + " / " + str(shorts))


def net_profit(mistake =None, setup=None):
    net = 0

    columns = ["pnl"]
    trades = call_db(columns, "trade_group", mistake, setup)
    for trade in trades:
        net += trade["pnl"]

    print(net)


def get_outcomes(mistake =None, setup=None):
    columns = ["outcome"]
    trades = call_db(columns, "trade_group", mistake, setup)
    for trade in trades:
        # print(str(trade.outcome) + "    ||     " + str(trade.pnl) + "     ||        " + str(trade.total_margin))
        print(trade["outcome"])


def get_rr_ratios(self, mistake=None, setup=None):

    columns = ["timestamp", "pnl","risk_reward"]
    trades = call_db(columns, "trade_group", mistake, setup)
    # benötigt 2 calls auf die Datenbank da hier auch single trades gefragt sind und nicht nur trade groups
    for trade in trades:
        if trade.risk_reward != None:
            print("TP: " + str(trade.open_trades[0].tp) + "  |  Price: "
                  + str(trade.open_trades[0].price) + "  |  SL: " + str(
                trade.open_trades[0].sl) + "  |  RR-Ratio: " + str(round(trade.risk_reward, 4)))
            # for open in trade.open_trades:
            # print(open.riskreward)
            # print(str(trade.risk_reward))
            # print(f"Index: {index}, Trade: {trade}")


def calc_profitfactor_month(mistake=None, setup=None):
    # get all trades within last 30 days
    thirty_days_ago_ms = round(time.time() * 1000) - (30 * 24 * 60 * 60 * 1000)
    lastmonth_list = []

    columns = ["timestamp","pnl"]
    trades = call_db(columns, "trade_group", mistake, setup)

    for trade in trades:
        if (trade["timestamp"] > thirty_days_ago_ms):
            lastmonth_list.append(trade)
    # get total wins and losses
    total_won = 0
    total_lost = 0
    for trade in lastmonth_list:
        # print(trade.pnl)
        if (trade["pnl"] >= 0):
            total_won += trade["pnl"]
        else:
            total_lost += trade["pnl"]

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


def get_longest_streak(self, mistake, setup):
    current_streak = 0
    longest_streak = 0
    current_streak_list = []
    longest_streak_list = []

    columns = ["position_ID", "outcome", "timestamp"]
    trades = call_db(columns, "trade_group", mistake, setup)

    for trade in trades:
        if trade["outcome"] == 1:
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
        print(str(tr["position_ID"]) + "   " + str(datetime.fromtimestamp(tr["timestamp"] / 1000.0, ))
              + "    " + str(tr["outcome"]))
    # return longest_streak, longest_streak_list

def new_call_db(user_id, columns=None, table=None, tag=None):
    conn = None
    cursor = None

    ALLOWED_TABLES = {"trade_group", "trade"}
    ALLOWED_COLUMNS = {
        # Trade table columns
        "trade_ID",  # (if present in your schema)
        "position_ID",
        "timestamp",
        "type",
        "price",
        "raw_profit",
        "profit",
        "leverage",
        "volume",
        "margin",
        "tp",
        "sl",
        "setup_tag",
        "mistake_tag",

        # trade_group table columns
        "user_ID",
        "side",
        "pair",
        "pnl",
        "tp_hit",
        "sl_hit",
        "be_point",
        "outcome",
        "fees",
        "risk_reward",
        "total_margin",
        "liqprice",
        "risk",
        "is_liquidated"
        }

    if table is not None:
        if table not in ALLOWED_TABLES:
            raise ValueError(f"Invalid table name: {table}")
    if columns is not None:
        for col in columns:
            if col not in ALLOWED_COLUMNS:
                raise ValueError(f"invalid column: {col}")

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Step 1: Get the tag_id for the tag name and user
        cursor.execute("""
                    SELECT tag_id FROM tags
                    WHERE name = %s AND user_ID = 1
                """, (tag))
        tag_row = cursor.fetchone()

        if not tag_row:
            return []  # No such tag found

        tag_id = tag_row['tag_id']
        # Step 2: Get all trade_group_ids with this tag
        cursor.execute("""
                    SELECT trade_group_id FROM trade_group_tags
                    WHERE tag_id = %s AND 
                """, (tag_id,))
        position_ids = [row['trade_group_id'] for row in cursor.fetchall()]

        if not position_ids:
            return []

        # Step 3: Fetch all trade_group rows for the found position_ids
        # Use IN clause to get all matching rows
        format_strings = ','.join(['%s'] * len(position_ids))
        query = f"""
                    SELECT * FROM trade_group
                    WHERE position_ID IN ({format_strings})
                """
        cursor.execute(query, position_ids)
        return cursor.fetchall()

        #---------------------------------------------------------------------------------------------------------

        tag_row = None

        if tag is not None:
            if isinstance(tag, str):
                cursor.execute("""
                           SELECT tag_id
                           FROM tags
                           WHERE name = %s 
                           """, tag)
            else:
                variable_string = ",".join(["&s"]*len(tag))
                query = f""" SELECT DISTINCT tag_id
                           FROM tags
                           WHERE name IN ({variable_string})"""
                cursor.execute(query, tag)

            tag_id = [row['tag_id'] for row in cursor.fetchall()]
            if not tag_id:
                return []

            #aufruf mit tag wenn einer gegeben ist
            id_string = ",".join(["%s"]*len(tag_id))

            # Step 2: Get all trade_group_ids with this tag
            cursor.execute(f"""
                           SELECT trade_group_id
                           FROM trade_group_tags
                           WHERE tag_id IN ({id_string})
                           """, (tag_id,))
            position_ids = [row['trade_group_id'] for row in cursor.fetchall()]

            if not position_ids:
                return []

            select = f"SELECT *"
            if columns is not None:
                cols = ",".join(columns)
                select = f"SELECT {cols}"

            from_table = f"FROM {table}"

            format = ",".join(["%s"]*len(position_ids))
            where = f"WHERE trade_group_id IN ({format})"

            query = " ".join([select, from_table, where])

            cursor.execute(query,position_ids)

        else:
            select = f"SELECT *"

            if columns is not None:
                cols = ",".join(columns)
                select = f"SELECT {cols}"

            from_table = f"FROM {table}"

            where = f"WHERE "




    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()




    pass
def call_db(columns=None, table=None, mistake=None, setup=None):
    """
    Quick way to access necessary database output in the form of a list of tuples. Will only return columns specified
    in columns param. table needs to be specified, otherwise trade_group is the default table.
    Cannot handle other WHERE filters besides mistake and setup tags

    :param columns: list of columns which should be included in SELECT
    :param table: specifies table from which function selects
    :param mistake: filter for WHERE
    :param setup: filter for WHERE
    :return: list of rows as tuples
    """
    conn = None
    cursor = None

    ALLOWED_TABLES = {"trade_group", "trade"}
    ALLOWED_COLUMNS = {
        # Trade table columns
        "trade_ID",  # (if present in your schema)
        "position_ID",
        "timestamp",
        "type",
        "price",
        "raw_profit",
        "profit",
        "leverage",
        "volume",
        "margin",
        "tp",
        "sl",
        "setup_tag",
        "mistake_tag",

        # trade_group table columns
        "user_ID",
        "side",
        "pair",
        "pnl",
        "tp_hit",
        "sl_hit",
        "be_point",
        "outcome",
        "fees",
        "risk_reward",
        "total_margin",
        "liqprice",
        "risk",
        "is_liquidated"
        }

    if table is not None:
        if table not in ALLOWED_TABLES:
            raise ValueError(f"Invalid table name: {table}")
    if columns is not None:
        for col in columns:
            if col not in ALLOWED_COLUMNS:
                raise ValueError(f"invalid column: {col}")

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # build query

        column_string = ", ".join(columns) if columns is not None else "*"
        table_string = f"{table}" if table is not None else "trade_group"
        base_query = f"SELECT {column_string} FROM {table_string}"
        conditions = []
        values = []

        if setup is not None:
            conditions.append("setup_tag = %s")
            values.append(setup)
        if mistake is not None:
            conditions.append("mistake_tag = %s")
            values.append(mistake)

        if conditions:
            query = base_query + " WHERE " + " AND ".join(conditions)
        else:
            query = base_query

        cursor.execute(query, values)
        result = cursor.fetchall()

        return result


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()





def long_short_winrate(mistake = None, setup = None):
    """
    iterates over all trades according to tags given in the function and calculates winrates for shorts and longs
    respectively. If no tags are given, calculates winrates for all trades in database

    :param mistake: mistake tag to filter
    :param setup: setup tag to filter
    :return: simply prints value, is not saved anywhere
    """
    columns = ["side", "outcome"]
    trades = call_db(columns, "trade_group", mistake, setup)

    longamount = 0
    longrate = 0
    shortamount = 0
    shortrate = 0
    for tr in trades:

        if tr["side"] == "2":
            shortamount += 1
            if tr["outcome"] == 1:
                shortrate += 1
        if tr["side"] == "4":
            longamount += 1
            if tr["outcome"] == 1:
                longrate += 1
    shortwinrate = (shortrate / shortamount) * 100
    longwinrate = (longrate / longamount) * 100

    return f"Winrate shorts: {shortwinrate} || Winrate longs: {longwinrate}"

    #return (" Winrate shorts: " + str(shortwinrate) + " || Winrate longs: " + str(longwinrate))




def get_tp_hitrate(mistake = None, setup = None):
    hits = 0
    trades = call_db(["tp_hit"], "trade_group", mistake, setup)
    for trade in trades:
        if trade["tp_hit"] == 1:
            hits += 1
    print("TP hitrate: " + str(round((hits / len(trades)) * 100, 2)) + "%")


def get_sl_hitrate(mistake = None, setup = None):
    hits = 0
    trades = call_db(["sl_hit"], "trade_group", mistake, setup)
    for trade in trades:
        if trade["sl_hit"] == 1:
            hits += 1
    print("SL hitrate: " + str(round((hits / len(trades)) * 100, 2)) + "%")


def avg_win_loss(self, mistake = None, setup = None):
    wins = 0
    winval = 0
    losses = 0
    lossval = 0

    trades = call_db(["outcome", "pnl"], "trade_group", mistake, setup)

    for tr in trades:
        if tr["pnl"] > 0:
            wins += 1
            winval += tr["pnl"]
        elif tr["pnl"] < 0:
            losses += 1
            lossval += tr["pnl"]

    avgwin = winval / wins
    avgloss = lossval / losses

    print("Average amount won: " + str(avgwin) + " || Average amount lost: " + str(avgloss))


def get_liquidations(mistake = None, setup = None):
    trades = call_db(["position_ID","is_liquidated" ], "trade_group", mistake, setup)
    liquidations = []

    for trade in trades:
        if trade["is_liquidated"] == 1:
            liquidations.append(trade["position_ID"])
