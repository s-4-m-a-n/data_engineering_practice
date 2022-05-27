import math

def get_frequency(first_date, last_date, total_post_count):
    frequency = {}

    total_days_betn_first_and_last_date = (last_date-first_date).days
    try:
      post_per_day = total_post_count/total_days_betn_first_and_last_date
      post_per_week = total_post_count/math.floor(total_days_betn_first_and_last_date/7) 
      post_per_month = total_post_count/math.floor(total_days_betn_first_and_last_date/30)

      frequency['post_per_day'] = post_per_day
      frequency['post_per_week'] = post_per_week
      frequency['post_per_month'] = post_per_month
    except ZeroDivisionError as e:
       frequency = {'post_per_week':None,'post_per_month':None}

    return frequency


def price_to_float(price:str,currency_minor_unit:int) -> float:
  price = float(price[:len(price) - currency_minor_unit]+'.'+price[len(price)-currency_minor_unit:])
  return price