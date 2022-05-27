import json

def is_dummy(item_string,kind="email",subtype="primary",dummy_records="dummy_data.json"):
    #loading json file
    with open(dummy_records,'r+') as file:
        dummy_data = json.loads(file.read())
    
    if item_string in dummy_data[kind][subtype]:
        return True
    else:
        return False
