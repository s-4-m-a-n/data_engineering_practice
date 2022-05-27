import difflib


#config
GEO_CODE_FILE_PATH = "../day 2/GeoGraphical_codes.csv"
CUTOFF_VALUE = 0.75
MAX_MATCH = 3



def csv_parser(file_path=GEO_CODE_FILE_PATH):
    ''' returns inverted index  '''
    #outpur inverted index data structure 
    inverted_index = {"district":{},
                      "municipality":{}
                }

    #parsing columns from the file
    with open(file_path,encoding="utf-8") as file:
        first_line = file.readline().replace("\n","")  
        columns_name = first_line.split(",")
      
        for line in file.readlines():
            line = line.replace("\n","").split(",")
            
            district_dict = inverted_index["district"]
            municipality_dict = inverted_index["municipality"]

            district_name = line[1]
            muni_name_eng = line[2]
            muni_name_nep = line[3]
            geo_code = line[5]
            
            #for disctrict
            if district_name not in district_dict.keys():
                district_dict[district_name] = [geo_code[:3]]
           
            #for municipality english
            if muni_name_eng in municipality_dict.keys():
                  municipality_dict[muni_name_eng].append(geo_code)
            else:
                  municipality_dict[muni_name_eng] = [geo_code]
            #for municipality nep
            if muni_name_nep in  municipality_dict.keys():
                  municipality_dict[muni_name_nep].append(geo_code)
            else:
                  municipality_dict[muni_name_nep] = [geo_code]


    return inverted_index


def get_intersection(close_districts,close_munis):
    ''' returns the municipality from the list of close municipality based on corresponding district available in the close district list'''
    matched_muni = []
    for muni in close_munis:
        if muni[:3] in close_districts:
            matched_muni.append(muni)
    return matched_muni


def get_geocode(input_district=None, input_municipality=None, allow_multiple = False) -> list:
    
    #return [] if there is no input value
    if input_district is None and input_municipality is None:
        return []

    #sanitizing input values
    district = ""
    municipality = ""
    if input_district:
        district = input_district.lower().strip()
    if input_municipality:
        municipality = input_municipality.lower().strip()

    #generating inverted file index
    inverted_index = csv_parser(GEO_CODE_FILE_PATH)
    muni_codes = []
    district_codes = []

    #handle spelling mistake
    #get all most words

    if input_municipality:
        municipality_close_match = difflib.get_close_matches(municipality,
                                                         inverted_index["municipality"].keys(), n = MAX_MATCH, cutoff=CUTOFF_VALUE)
    if input_district:
        district_close_match = difflib.get_close_matches(district,
                                                     inverted_index["district"].keys(),n = MAX_MATCH, cutoff=CUTOFF_VALUE)

    
    #getting codes
    if input_municipality:
        for muni in municipality_close_match:
            muni_codes = muni_codes + inverted_index["municipality"][muni]
    if input_district:
        for dist in district_close_match:
            district_codes = district_codes + inverted_index["district"][dist]

    #removing redundant values
    muni_codes = list(set(muni_codes))
    district_codes = list(set(district_codes))
  
    
    #case 1
    if input_district is None and input_municipality :
        if len(muni_codes) == 1:
            return muni_codes[0]
        elif len(muni_codes) != 1 and allow_multiple:
            return muni_codes
        else:
            return []
    #case 2
    elif input_district and input_municipality is None:
        if len(district_codes) == 1:
            return district_codes[0]
        elif len(district_codes) != 1 and allow_multiple:
            return district_codes
        else:
            return []
        

    #case 3
    elif input_municipality and input_district:
        #finding the intersection value between the close_match of muni and district
        closest_match = []
        if len(muni_codes) >= 1:  #if multiple municipality
          closest_match = get_intersection(district_codes, muni_codes)
          if len(closest_match) == 1:  #if there is exactly one item then no need to process further
              return closest_match[0]
          elif len(closest_match) > 1 and allow_multiple:
              return closest_match
          else:
              return []




if __name__ == '__main__':
	print(get_geocode("taplejug",None))