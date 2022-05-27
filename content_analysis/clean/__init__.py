#from indexpress.analysis.ecommerce import some_function

# Perform analysis in this function and return it in the
# format as specified in ../schema.txt

import json
import wordpress_analysis 
import woocommerce_analysis
import shopify.shopify_analysis

import __extra__.wordpress__extra as wordpress__extra
import __extra__.woocommerce__extra as woocommerce__extra

#--config---
SCHEMA_PATH = "content_template.json"
EXTRA_SCHEMA_PATH = "__extra__/__extra__schema.json"

def load_template(SCHEMA_PATH):
	template_json = None
	with open(SCHEMA_PATH) as f:
		template_json = json.load(f)
	return template_json


def content_analysis(content = None, meta=None, platform=None):
	
	with open("allbirds.json") as f:
		content= json.load(f)
	

 
	# CONTENT_OBJ = content

	#loading analysis response template and __extra__ json template inside response template
	analysis_result = load_template(SCHEMA_PATH)
	analysis_result["__extra__"] =  load_template(EXTRA_SCHEMA_PATH)
 
	#======================== wordpress ====================================
	#for wordpress website
	if content.get('wordpress',False):
		print("ok")
		analysis_result = wordpress_analysis.analysis(content,analysis_result)
		#add __extra__
		wp__extra = wordpress__extra.generate(content)
		analysis_result["__extra__"].update(wp__extra)
  
		#================================woocommerce=====================================
		# if it is an ecommerce site (or woocommerce section is provided)
		if content.get('woocommerce',False):
			analysis_result = woocommerce_analysis.analysis(content,analysis_result)
			#add __extra
			wc__extra = woocommerce__extra.generate(content)
			analysis_result["__extra__"].update(wc__extra)
   
	#for shopify site
	elif content.get('shopify',False):
		analysis_result = shopify_analysis.analysis(content,analysis_result)
	
	#save the analysis_result in a json file  
	with open("response.json","w") as f:
		json.dump(analysis_result,f)
  
	print("save")
 
	return analysis_result    


if __name__ =="__main__":
	content_analysis()