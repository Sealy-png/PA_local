from close_trade import Close_Trade
from open_trade import Open_Trade



import mysql.connector





def get_connection():
    return mysql.connector.connect(
    host="localhost",         # oder die IP-Adresse deines MySQL-Servers
    user="root",
    password="root",
    database="pa_db"
)

def add_trade(trade):
    """
    adds an open/close trade to the trade table.

    :param trade: open_trade/close_trade object
    :return: void
    """
    conn = get_connection()
    cursor = conn.cursor()



    trade_type = None
    if isinstance(trade, Close_Trade):
        trade_type = "close"
    elif isinstance(trade, Open_Trade):
        trade_type = "open"

    query = """
            INSERT INTO trade (
                position_ID, timestamp, type, price, raw_profit, profit,
                leverage, volume, margin, tp, sl
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

    values = (
        trade.position_ID,
        trade.timestamp,
        trade_type,
        getattr(trade, 'price', None),
        getattr(trade, 'raw_profit', None),
        getattr(trade, 'profit', None),
        getattr(trade, 'leverage', None),
        getattr(trade, 'volume', None),
        getattr(trade, 'margin', None),
        getattr(trade, 'tp', None),
        getattr(trade, 'sl', None),
        )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def check_existing_trade(position_ID):
    """
    Checks if a trade is already in the Database

    :param position_ID:
    :return: exists: Boolean value, True = exists, False = doesn't exist
    """
    pass

def add_trade_group(trade_group):
    """
    Adds a trade_group to the trade_group table
    :param trade_group: trade group object to be added to the table
    :return: void
    """
    pass



def extract_from_database(user_ID):
    pass

