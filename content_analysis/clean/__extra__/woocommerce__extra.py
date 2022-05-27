from indexpress.analysis.__extra__.helper_functions import *

def generate(CONTENT_OBJ):
    __extra__data = {}
    #category frequency-------------------------------
    category_set_1 = [(category['name']).lower() for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products'] 
                for category in product['categories']]  #captured from products 
    category_hist = histogram_generator(category_set_1)
    #filling __extra__data field
    __extra__data['category_freq'] = category_hist


    #tag frequency------------------------------------
    tag_list = [(category['name']).lower() for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products'] 
                for category in product['tags']] 
    tag_hist = histogram_generator(tag_list)
    #filling __extra__data field
    __extra__data['tag_freq'] = tag_hist


    #category vs price -------------------------------
    category_price = {}

    #category price
    for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products']:
        for category in product['categories']:
            if category['name'].lower() not in category_price.keys():
                category_price[category['name'].lower()] = list([int(product['prices']['price'])/100])
            else:
                category_price[category['name'].lower()].append(int(product['prices']['price'])/100)

    #filling __extra_data field
    __extra__data['category_price_range']= range_generator(category_price)
    __extra__data['category_avg_price'] = avg_generator(category_price)

    #category vs discount-------------------------------------------------
    category_discount = {}

    for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products']:
        for category in product['categories']:
            if category['name'].lower() not in category_discount.keys():
                category_discount[category['name'].lower()] = list([int(product['prices']['regular_price'])/100 - int(product['prices']['sale_price'])/100 ])
            else:
                category_discount[category['name'].lower()].append(int(product['prices']['regular_price'])/100 - int(product['prices']['sale_price'])/100)

    #filling __extra__data field
    __extra__data['category_discount_range'] = range_generator(category_discount)
    __extra__data['category_avg_discount'] = avg_generator(category_discount)

    #category vs average rating--------------------------------------------------
    category_rating = {}
    for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products']:
        for category in product['categories']:
            rating = int(product['average_rating'])
            rating = rating if rating >= 0 else 0
            if category['name'].lower() not in category_rating.keys():
                category_rating[category['name'].lower()] = list([rating])
            else:
                category_rating[category['name'].lower()].append(rating)

    #filling __extra__data field
    __extra__data['category_rating_range'] = range_generator(category_rating)
    __extra__data['category_avg_rating'] = avg_generator(category_rating)

    #category review-------------------------------------------------------------
    category_review = {}
    for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products']:
        for category in product['categories']:
            review = int(product['review_count'])
            review = review if review >= 0 else 0
            if category['name'].lower() not in category_review.keys():
                category_review[category['name'].lower()] = list([review])
            else:
                category_review[category['name'].lower()].append(review)

    #filling __extra__data field
    __extra__data['category_review_range'] = range_generator(category_review)
    __extra__data['category_avg_review'] = avg_generator(category_review)

    return __extra__data