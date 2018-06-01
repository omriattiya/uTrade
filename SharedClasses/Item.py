class Item:
    def __init__(self, id, shop_name, name, category, keywords, price, quantity, kind,
                 url, item_rating, sum_of_rankings, num_of_reviews):
        self.id = id
        self.shop_name = shop_name
        self.name = name
        self.category = category
        self.keyWords = keywords
        self.price = price
        self.quantity = quantity
        self.kind = kind
        self.item_rating = item_rating
        self.sum_of_rankings = sum_of_rankings
        self.num_of_reviews = num_of_reviews
        if url is None:
            self.url = "http://www.tea-tron.com/antorodriguez/blog/wp-content/uploads/2016/04/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png"
        else:
            self.url = url
