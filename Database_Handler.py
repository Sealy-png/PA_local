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


# Determine wether trade is open
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
        trade.positionID,
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT position_ID FROM trade_group WHERE position_ID = %s
        """, (position_ID,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    exists = result is not  None
    return exists

def add_tag(user_id, tag_name):
    """
    Adds a new tag for a specific user to the tags table. tag_id is auto increment, no assignment needed.

    :param user_id: ID of the user creating the tag
    :param tag_name: Name of the tag to add
    :return: void
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if tag already exists for the user
        cursor.execute("""
                    SELECT 1 FROM tags
                    WHERE user_ID = %s AND name = %s
                """, (user_id, tag_name))

        if cursor.fetchone():
            print(f"Tag '{tag_name}' already exists for user {user_id}.")
            return

        # Execute if tag-trade pair doesn't exist

        cursor.execute("""
            INSERT INTO tags (user_ID, name)
            VALUES (%s, %s)
        """, (user_id, tag_name))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_user_tag_ids(user_id):
    """
    Retrieves all tag IDs for a specific user.

    :param user_id: ID of the user
    :return: List of tag IDs belonging to the user
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT tag_ID FROM tags WHERE user_ID = %s
        """, (user_id,))
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        cursor.close()
        conn.close()


def add_tag_to_trade_group(position_id, tag_id):
    """
    Assigns

    :param position_id:
    :param tag_id:
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
                    SELECT 1 FROM trade_group_tags
                    WHERE trade_group_id = %s AND tag_id = %s
                """, (position_id, tag_id))

        if cursor.fetchone():
            print(f"Tag ID {tag_id} is already assigned to trade group {position_id}.")
            return

        cursor.execute("""
            INSERT INTO trade_group_tags (trade_group_id, tag_id)
            VALUES (%s, %s)
        """, (position_id, tag_id))

        conn.commit()
    finally:
        cursor.close()
        conn.close()



def add_trade_group(trade_group, setup_tag= None, mistake_tag=None):
    """
    Adds a trade_group to the trade_group table
    :param trade_group: trade group object to be added to the table
    :return: void
    """
    cancel = check_existing_trade(getattr(trade_group, 'positionId'))

    # if Check for existing trade returns true, insertion is cancelled.
    if cancel:
        return


    conn = get_connection()
    cursor = conn.cursor()



    query = """
                INSERT INTO trade_group (
                    user_ID, position_ID, side, pair, price, pnl, tp_hit, sl_hit, be_point, 
                    outcome, fees, risk_reward, timestamp,
                    total_margin, liqprice, risk, is_liquidated, setup_tag, mistake_tag
                    
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

    values = (
        1,
        getattr(trade_group, 'positionId'),
        getattr(trade_group, 'side'),
        getattr(trade_group, 'pair'),
        getattr(trade_group, 'price'),
        getattr(trade_group, 'pnl'),
        getattr(trade_group, 'tp_hit'),
        getattr(trade_group, 'sl_hit'),
        getattr(trade_group, 'be_point'),
        getattr(trade_group, 'outcome'),
        getattr(trade_group, 'fees'),
        getattr(trade_group, 'risk_reward'),
        getattr(trade_group, 'timestamp'),
        getattr(trade_group, 'total_margin'),
        getattr(trade_group, 'liqprice'),
        getattr(trade_group, 'risk'),
        getattr(trade_group, 'is_liquidated'),
        setup_tag,
        mistake_tag # Both tags are optional
    )
    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    for trade in trade_group.open_trades:
        add_trade(trade)

    for trade in trade_group.close_trades:
        add_trade(trade)




def extract_from_database(user_ID):
    pass

