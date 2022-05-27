from helper_functions import *
import math
import numpy as np

def analysis(CONTENT_OBJ, analysis_result):
    '''performs analysis on content obj'''

    product_obj = CONTENT_OBJ['woocommerce']['edges']['wc/store/products']
            
    products_count =  CONTENT_OBJ['woocommerce']['count']['wc/store/products']

    #tags fetching-------------------------------------------------
    #capturing from products properties
    tag_set_1 = set([ (tag['name']).lower() for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products'] 
            for tag in product['tags']])
            
    #captured from products/tags properties        
    tag_set_2 = set([(tag['name']).lower() for tag in CONTENT_OBJ['woocommerce']['edges']['wc/store/products/tags']])
    
    #union 
    tag_list = list(tag_set_1.union(tag_set_2))

    #capturing categories---------------------------------------------
    category_set_1 = set([ (category['name']).lower() for product in CONTENT_OBJ['woocommerce']['edges']['wc/store/products'] 
            for category in product['categories']])  #captured from products 

    #captured from product tags               
    category_set_2 = set([(category['name']).lower() for category in CONTENT_OBJ['woocommerce']['edges']['wc/store/products/categories']])

    #union 
    category_list = list(category_set_1.union(category_set_2))

    #capturing 
    #reading prices-------------------------------------
    price_list = [price_to_float(product['prices']['price'],product['prices']['currency_minor_unit'])\
                    if product['prices']['currency_minor_unit'] is not None \
                    else price_to_float(product['prices']['price'],0)\
                    for product in product_obj]

    # currency_code_list = set([product['prices']['currency_code'] for product in product_obj])
    #price analysis--------------------------------------
    min_price = min(price_list)
    max_price = max(price_list)
    # avg_price = np.mean(price_list)

    q1 = np.quantile(price_list,0.25)
    q2 = np.quantile(price_list,0.5)
    q3 = np.quantile(price_list,0.75)

    # price_sd = np.std(price_list)
    # price_var = price_sd**2 

    
    #preparing output ------------------------------------------
    # 'cms': {
    #             'topic': [],
    #             'frequency': {
    #               'week': None,
    #               'month': None
    #             },
    #             'count': {
    #               'category': None,
    #               'post': None,
    #               'author': None
    #             }
    #           }
    analysis_result['ecommerce']['topic']= list(set(tag_list + category_list))
    analysis_result['ecommerce']['price'] = {'high' : max_price , 
                                                'upper_average':q3 ,
                                                'average':q2 ,
                                                'lower_average' : q1 ,
                                                'low' :min_price }
    analysis_result['ecommerce']['count'] = {'category':len(category_list),'product':products_count}

    return analysis_result