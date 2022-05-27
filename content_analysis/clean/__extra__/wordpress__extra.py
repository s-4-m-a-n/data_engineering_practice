from datetime import datetime

def generate(CONTENT_OBJ):
    __extra__data = {}
    #cms __extra__data----------------------------------
    #post frequency per year
    post_date = {} 
    for post in CONTENT_OBJ['wordpress']['edges']['wp/v2/posts']: #two post doesnt have a same id
            post_date[post['id']] = datetime.strptime(post['date'],"%Y-%m-%dT%H:%M:%S")

    post_count_per_year = {}
    for key in post_date.keys():
        year = post_date[key].year
        if year not in post_count_per_year.keys():
            post_count_per_year[year] = 1
        else:
            post_count_per_year[year] += 1
            
    #filling __extra__data field
    __extra__data['post_count_per_year'] = post_count_per_year
    
    return __extra__data