from nthrow.source.simple import SimpleSource
import re, json
from nthrow.utils import sha1


def quantity_parser(name):
    # normalizing the text
    name = ' '.join(name.split()).lower()
    amount_pattern  = re.compile("([0-9]+ [a-z]+|[0-9]+[a-z]+)")
    find = amount_pattern.search(name)
    amount = find.group(1)

    price_unit = re.compile("([0-9]+)\ ?([a-z]+)")
    find = price_unit.search(amount)
    return {"qty": find.group(1),"qty_unit": find.group(2)}

def name_parser(name):
    # normalizing the text
    name = ' '.join(name.split()).lower()

    hyphen_search = re.compile("-\ ?[0-9]+").search(name)
    hyphen_sub_str = hyphen_search.group() if hyphen_search else ''

    hyphen_index = name.find(hyphen_sub_str) 

    by_index = name.find("by")

    num_search = re.compile("[0-9]+").search(name)
    num_sub_str = num_search.group() if num_search else ''

    num_index = name.find(num_sub_str)
    indexes = []
    for num in [hyphen_index, by_index, num_index]:
        if num != -1 and num != 0:
            indexes.append(num)

    index = min(indexes) if len(indexes) > 0 else None
    return {"product_name":name[:index].strip()}

def parse_response(response_txt):
    interested_keys = ["productUrl","name","nid", "image", "price","ratingScore","review", "location", "brandId","brandName","sellerId","sellerName"]
    filtered_product_data = []
    for item in json.loads(response_txt)["mods"]["listItems"]:
        filtered_item = {} 
        for key in interested_keys:
            filtered_item[key] = item[key]
            if key == "name": # extracting information from name or product title
                name = item[key]
                filtered_item.update(quantity_parser(name))
                filtered_item.update(name_parser(name))

        filtered_product_data.append(filtered_item)
    return filtered_product_data





class Extractor(SimpleSource):
    def __init__(self, *args, **kwargs):
        super(Extractor, self).__init__(*args, **kwargs)
    
    def make_url(self, row, _type):
        # args is dict that contains current page cursor, limit and other variables from extractor.query_args, extractor.settings
        args = self.prepare_request_args(row, _type)
        page = args['cursor'] or 1
        return f'https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input&page={page}&q=nuts', page

    
    async def fetch_rows(self, row, _type='to'):
		# row is info about this datset
		# it is what was returned with extractor.get_list_row method
		# it holds pagination, errors, retry count, next update time etc.
        try:
            url, page = self.make_url(row, _type)
            res = await self.http_get(url)	# wrapper around aiohttp session's get
            
            if res.status == 200:
                content = await res.text()
                content = parse_response(content)
                
                rows = [
                    {
                        'uri': self.mini_uri("http:"+e.get("productUrl"), parameters=('search')) ,
                        'product': e
                    }
                    for i,e in enumerate(content)
                ]

                rows = self.clamp_rows_length(rows)	# slice rows length to limit from extractor.query_args or extractor.settings[remote]
                return {
                    'rows': [
                        self.make_a_row(row['uri'], self.mini_uri(r['uri']), r) for r in rows
                    ],
                    'state': {
                        'pagination': {
                            # value for next page, return None when pagination ends
                            _type: page+1
                        }
                    }
                }

            else:
                self.logger.error('Non-200 HTTP response: %s : %s' % (res.status, url))
                return self.make_error('HTTP', res.status, url)

        except Exception as e:
            self.logger.exception(e)
            return self.make_error('Exception', type(e), str(e))