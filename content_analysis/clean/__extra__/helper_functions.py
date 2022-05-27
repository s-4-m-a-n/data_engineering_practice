import numpy as np

def range_generator(dict_obj):
    '''
    convert the dict obj of list value into range
    '''
    range_dic = {}
    for item in dict_obj.keys():
        range_dic[item]= {"min":min(dict_obj[item]),
                                            "mid":np.median(dict_obj[item]),
                                            "max":max(dict_obj[item])}
    return range_dic


def avg_generator(dict_obj):
    '''
    calculate average of each list itemset of the the dict obj item
    '''
    avg_dic = {}
    for item in dict_obj.keys():
        avg_dic[item]= np.mean(dict_obj[item])
    return avg_dic


def histogram_generator(obj_list):
    '''
    convert the list into histogram
    '''
    hist = {}
    for item in obj_list:
        if item in hist:
            hist[item] += 1
        else:
            hist[item] = 1
    return hist