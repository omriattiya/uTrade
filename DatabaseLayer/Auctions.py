from DatabaseLayer.getConn import commit_command, select_command


def fetch_integer(result):
    if len(result) == 0:
        return False
    return result[0]


def bid_on_item(auction_bid):
    sql_query = """
                INSERT INTO AuctionCustomers(auction_id,username,price)
                VALUES ('{}','{}','{}')
                """.format(auction_bid.auction_id, auction_bid.username, auction_bid.price)
    return commit_command(sql_query)


def get_max_bid(auction_id):
    sql_query = """
                    SELECT SUM(price)
                    FROM AuctionCustomers
                    WHERE auction_id = '{}'
                """.format(auction_id)
    return fetch_integer(select_command(sql_query))


def add_auction(auction):
    sql_query = """
                    INSERT INTO Auctions(auction_id,end_date)
                    VALUES ('{}','{}')
                    """.format(auction.auction_id, auction.end_date)
    return commit_command(sql_query)
