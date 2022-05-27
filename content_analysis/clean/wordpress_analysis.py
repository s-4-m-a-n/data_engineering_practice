from helper_functions import *
from datetime import datetime
import math

def analysis(CONTENT_OBJ,analysis_result):
	
	wordpress_post_obj = CONTENT_OBJ['wordpress']['edges']['wp/v2/posts']

	#fetching wordpress counts------------------------------------------------
	post_count = CONTENT_OBJ['wordpress']['count']['wp/v2/posts']
	
	post_category_list = list(set([category for post in wordpress_post_obj for category in post['categories']]))
	post_category_count = len(post_category_list)

	#author count
	post_authors = [] 
	for post in wordpress_post_obj:
		for author_properties in post['_embedded']['author']:
			post_authors.append(author_properties['id'])

	author_count = len(post_authors)


	media_count = CONTENT_OBJ['wordpress']['count']['wp/v2/media']
	page_count = CONTENT_OBJ['wordpress']['count']['wp/v2/pages']

	#fetching wordpress --> edges --> posts ----------------------------------

	post_date_list =[datetime.strptime(post['date'],"%Y-%m-%dT%H:%M:%S") for post in wordpress_post_obj]
	post_date_list.sort()

	first_post_date = None
	last_post_date =None
	
	if post_date_list[0]: # if there exists any posts
		first_post_date = post_date_list[0]
		last_post_date = post_date_list[-1]

	cms_freq = get_frequency(first_post_date,last_post_date,post_count)

	#preparing output
	#  'cms': {
	#                   'topic': [],
	#                   'frequency': {
	#                     'week': None,
	#                     'month': None
	#                   },
	#                   'count': {
	#                     'category': None,
	#                     'post': None,
	#                     'author': None
	#                   }
	#                 }
	analysis_result['cms']['topic'] = post_category_list
	analysis_result['cms']['frequency'] = {'week':cms_freq['post_per_week'], 
											'month' : cms_freq['post_per_month']}
	analysis_result['cms']['count'] = {'category' : post_category_count,
										'post' : post_count, 
										'author' : author_count }

	return analysis_result