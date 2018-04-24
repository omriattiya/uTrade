from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.Auction import Auction


def fetch_integer(result):
    if len(result) == 0:
        return False
    result = result[0]
    if result[0] is None:
        return False
    return result[0]


def fetch_auction(auction):
    if len(auction) == 0:
        return False
    auction = auction[0]
    auction = Auction(auction[0], auction[1])
    return auction


def fetch_auctions(auctions):
    auction_arr = []
    for auction in auctions:
        auction_arr.append(Auction(auction[0], auction[1]))
    return auction_arr


def bid_on_item(auction_bid):
    sql_query = """
                INSERT INTO AuctionCustomers(auction_id,username,price)
                VALUES ('{}','{}','{}')
                """.format(auction_bid.auction_id, auction_bid.username, auction_bid.price)
    return commit_command(sql_query)


def get_max_bid(auction_id):
    sql_query = """
                    SELECT MAX(price)
                    FROM AuctionCustomers
                    WHERE auction_id = '{}'
                """.format(auction_id)
    return fetch_integer(select_command(sql_query))


def get_auction(auction_id):
    sql_query = """
                    SELECT *
                    FROM Auctions
                    WHERE auction_id = '{}'
                """.format(auction_id)
    return fetch_auction(select_command(sql_query))


def get_all_auctions():
    sql_query = """
                    SELECT *
                    FROM Auctions
                """
    return fetch_auctions(select_command(sql_query))


def add_auction(auction):
    sql_query = """
                    INSERT INTO Auctions(auction_id,end_date)
                    VALUES ('{}','{}')
                    """.format(auction.auction_id, auction.end_date)
    return commit_command(sql_query)
