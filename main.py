import random

import Trade_Analyzer
import mexc_api
import mexc_api as mexc
import user
import datetime
from open_trade import Open_Trade
from close_trade import Close_Trade
from trade_group import Trade_Group
import datetime
import time
import mysql.connector
import json
from tabulate import tabulate
from random import randrange

import Database_Handler

#korrekter api call
#trades = mexc.get_history_orders(testuser.api_key, testuser.api_secret, start_time='1733055283000', end_time= '1735647614000', page_size='100',)['data']




def test_group_trades_by_key(user):
    testuser = user
    history = mexc.get_history_orders(testuser.api_key, testuser.api_secret, page_size='100', )['data']
    trades = testuser.group_trades_by_key(history)

    for position_id, trades_list in trades.items():
        print(f"Position ID: {position_id}")
        for trade in trades_list:
            print(trade)
        print()
    print(len(trades))

def test_get_trades_mexc(user):
    testuser = user
    testuser.get_trades_mexc()
    #print(testuser.trade_list[0].positionId)
    print(len(testuser.trade_list))




def get_potential_liquidations():
    #trades = mexc.get_history_orders("mx0vglQex9FqRaEn23", "69ad91c2428149f290c779549cf4cf1e")['data']
    history = mexc.get_history_orders("mx0vgl0fxT1zFO7oxA", "6dd81fbf142b43d39def9cc29990c136", start_time=1730415600000, end_time=1737591241739, page_size='100')['data']
    for trade in history:
        #if trade['positionId'] == 614813654 or trade['positionId'] == 611556583:
        print(trade)




def get_connection():
    return mysql.connector.connect(
    host="localhost",         # oder die IP-Adresse deines MySQL-Servers
    user="root",
    password="root",
    database="pa_db"
)


def get_trade_groups():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM trade_group")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

    cursor.close()
    conn.close()

def get_tags():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tags")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

    cursor.close()
    conn.close()


def get_trade_tags():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM trade_group_tags")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

    cursor.close()
    conn.close()


def get_single_trade():
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch all rows from the user table
    cursor.execute("SELECT * FROM trade")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

    cursor.close()
    conn.close()

def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch all rows from the user table
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

    cursor.close()
    conn.close()

def get_user_account():
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch all rows from the user table
    cursor.execute("SELECT * FROM user_account")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Get column names

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

    cursor.close()
    conn.close()

def show_tables():
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch all rows from the user table
    cursor.execute("SHOW TABLES")
    users = cursor.fetchall()

    # Print each row
    for user in users:
        print(user)

    cursor.close()
    conn.close()

def wipe_trade_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Use DELETE to preserve structure and avoid FK issues
    cursor.execute("DELETE FROM trade")
    cursor.execute("DELETE FROM trade_group")

    conn.commit()
    cursor.close()
    conn.close()

def quick_add_db():
    testuser = user.User("mx0vgllVKkGlQJ7cYg", "424ec2cc1b794079a539755577e8638b")
    testuser.set_be_point(10)
    history = mexc.get_history_orders(testuser.api_key, testuser.api_secret, page_size='100', )['data']
    trades = testuser.group_trades_by_key(history)
    testuser.create_trade_groups(trades)

    testuser.add_list_to_database()




def drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Drop tables individually
        tables = ["trade", "trade_group_tags", "tags", "trade_group", "user"]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user_tag_ids(user_id):
    """Returns a list of tag_ids for a given user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT tag_id FROM tags WHERE user_ID = %s
        """, (user_id,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()




def main():
    tags1 = ["test"]
    tags2 = ["test2"]

    setup =["test","test2"]


    #get_user_account()
    get_trade_groups()
    #wipe_trade_tables()
    #quick_add_db()
    #get_single_trade()


    #-------------------------------------------------------------------------
    #Noch zu testen:
    #Trade_Analyzer.trade_frequency_by_day()
    #Trade_Analyzer.trade_frequency_by_week()
    #print(Trade_Analyzer.trade_group_count(1))
    #Trade_Analyzer.risk_vs_accountsize("MEXC")
    Trade_Analyzer.positionsize_vs_pnl(1)

    # ------------------------------------------------------------------------
    #Bereits getestet:

    #get_trade_groups()
    #print(Trade_Analyzer.get_winrate(tags1))
    #Trade_Analyzer.long_short_ratio()
    #Trade_Analyzer.net_profit()
    #Trade_Analyzer.get_outcomes()
    #Trade_Analyzer.get_rr_ratios()
    #print(Trade_Analyzer.calc_profitfactor_month())
    #Trade_Analyzer.get_longest_streak()
    #Trade_Analyzer.get_pnls()
    #print(Trade_Analyzer.long_short_winrate())
    #show_tables()
    #get_trade_groups()
    #Trade_Analyzer.get_sl_hitrate()
    #Trade_Analyzer.long_short_ratio()
    #Trade_Analyzer.avg_win_loss()






if __name__ == '__main__':
    main()


"""


CREATE TABLE trade_group_tags (
    trade_group_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (trade_group_id, tag_id),
    FOREIGN KEY (trade_group_id) REFERENCES trade_group(group_ID) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);

CREATE TABLE tags (
    tag_id INT NOT NULL AUTO_INCREMENT,
    user_ID INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (tag_id),
    FOREIGN KEY (user_ID) REFERENCES user(user_ID) ON DELETE CASCADE
);

CREATE TABLE user (
    USER_ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    level INT,
    API_KEY VARCHAR(255),
    API_SECRET VARCHAR(255),
    PRIMARY KEY (USER_ID)
);

CREATE TABLE trade_group (
    group_ID INT NOT NULL AUTO_INCREMENT,
    user_ID INT NOT NULL,
    position_ID INT NOT NULL,
    side VARCHAR(5),
    pair VARCHAR(20),
    price DOUBLE,
    pnl DOUBLE,
    tp_hit TINYINT(1),
    sl_hit TINYINT(1),
    be_point DOUBLE,
    outcome TINYINT,
    fees DOUBLE,
    risk_reward DOUBLE,
    timestamp BIGINT,
    total_margin DOUBLE,
    liqprice DOUBLE,
    risk DOUBLE,
    is_liquidated TINYINT(1),
    setup_tag VARCHAR(25),
    mistake_tag VARCHAR(25),
    PRIMARY KEY (group_ID),
    INDEX (user_ID)
);


CREATE TABLE trade (
    trade_ID INT NOT NULL AUTO_INCREMENT,
    position_ID INT NOT NULL,
    type VARCHAR(25),
    timestamp BIGINT NOT NULL,
    price DOUBLE,
    raw_profit DOUBLE,
    profit DOUBLE,
    leverage DOUBLE,
    volume DOUBLE,
    margin DOUBLE,
    tp DOUBLE,
    sl DOUBLE,
    group_ID INT,
    PRIMARY KEY (trade_ID),
    INDEX (position_ID),
    INDEX (group_ID),
    FOREIGN KEY (group_ID) REFERENCES trade_group(group_ID) ON DELETE CASCADE
);

"""