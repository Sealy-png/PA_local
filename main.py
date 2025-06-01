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
    testuser.set_be_point(0.1)
    history = mexc.get_history_orders(testuser.api_key, testuser.api_secret, page_size='100', )['data']
    trades = testuser.group_trades_by_key(history)
    testuser.create_trade_groups(trades)

    testuser.add_list_to_database()


"""
CREATE TABLE trade_group (
    user_ID INT NOT NULL,
    position_ID INT NOT NULL PRIMARY KEY,
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
    INDEX (user_ID)  -- corresponds to 'MUL' on user_ID
);

CREATE TABLE trade (
    trade_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
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
    INDEX (position_ID)
);


CREATE TABLE user (
    USER_ID INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    level INT,
    API_KEY VARCHAR(255),
    API_SECRET VARCHAR(255)
);


"""



def main():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
   
CREATE TABLE trade_group (
    user_ID INT NOT NULL,
    group_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
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
    INDEX (user_ID)  -- corresponds to 'MUL' on user_ID
);
    """)

    conn.commit()

    cursor.close()
    conn.close()


    #get_trade_groups()







if __name__ == '__main__':
    main()