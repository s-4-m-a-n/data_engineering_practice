from helper_functions import get_frequency
from datetime import datetime
import math

def analysis(content,analysis_result):
    
    vendor_list = []
    price_list  = []
    for product in CONTENT_OBJ['shopify']['edges'].get('products.json',False):
        #vendor list capturing
        if product.get('vendor',False):
            vendor_list.append(product.get('vendor'))
        
        #price list capturing
        for variants in product.get('variants',[]):
            price_list.append(float(variants.get('price',"0")))
        
            
        #product post date capturing
        if product.get('published_at',False):
            product_post_date.append(datetime.strptime(product['published_at'][:19],"%Y-%m-%dT%H:%M:%S"))
        if product.get('updated_at',False):
            product_post_date.append(datetime.strptime(product['updated_at'][:19],"%Y-%m-%dT%H:%M:%S"))
            
        if product_post_date[0]: # if there exists any posts
            first_post_date = product_post_date[0]
            last_post_date = product_post_date[-1]
    
        post_freq = get_frequency(first_post_date,last_post_date,len(product_post_date))
    
    #product post frequency
    price_dict = {"high":max(price_list),
                  "upper_average":np.quantile(price_list,0.75),
                  "average":np.quantile(price_list,0.5),
                  "lower_average":np.quantile(price_list,0.25),
                  "low":min(price_list)}
    
        
    # count product
    products_count = 0
    for collection in CONTENT_OBJ['shopify']['edges'].get('collections.json',False):
        products_count += collection.get('products_count',0)
        
    #filling analysis_result field------------output generation---------------------
    analysis_result['ecommerce']['vendor'] = vendor_list
    analysis_result['ecommerce']['price'] = price_dict
    analysis_result['ecommerce']['frequency'] = {'week':post_freq['post_per_week'], 
                                                 'month' : post_freq['post_per_month']}
    analysis_result['ecommerce']['count']['product'] = products_count
    
    
    return analysis_result