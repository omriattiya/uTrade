from datetime import datetime
from DatabaseLayer import Auctions, Items
from DatabaseLayer.Auctions import get_auction
from DomainLayer import ItemsLogic
from SharedClasses.Auction import Auction


def bid_on_item(auction_bid):
    if auction_bid is not None:
        auction = get_auction(auction_bid.auction_id)
        final_date = datetime.strptime(auction.end_date, '%Y-%m-%d')
        minimal_amount = get_minimal_amount(auction_bid.auction_id)
        if auction_bid.price > minimal_amount and final_date > datetime.now():
            return Auctions.bid_on_item(auction_bid)
    return False


def add_auction(item, username, end_date):
    if item is not None and username is not None and end_date is not None:
        final_date = datetime.strptime(end_date, '%Y-%m-%d')
        if final_date > datetime.now():
            item_id = ItemsLogic.add_item_to_shop_and_return_id(item, username)
            if item_id is False:
                return False
            auction = Auction(item_id, end_date)
            return Auctions.add_auction(auction)
    return False


def get_minimal_amount(auction_id):
    ret = Auctions.get_max_bid(auction_id)
    if ret is False:
        return Items.get_item(auction_id).price
    return ret