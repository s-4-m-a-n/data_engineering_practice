import os
import json
import pandas as pd

def unpack_list(data,columns=["primary_email","secondary_email"]):
    data_list = []
    for col in columns:
        if col in data.columns:
            for item in data[col]:
                data_list += str(item).strip('][').replace('"',"").split(', ')
    return data_list
    

def dummy_items_collector(dataframe,columns=['primary_email','secondary_email'],threshold=20,save_to="json",json_file="dummy_data.json"):
    kind = columns[0].split('_')[1]
    if len(columns)>1:
        file_name = "dummy_"+str(kind)
    else:
        file_name="dummy_"+columns[0]
    try:
        item_list = unpack_list(dataframe,columns=columns)
        print(f"length of total {kind} : {len(item_list)}")
        item_list = pd.DataFrame(item_list,columns=[kind])
        item_freq_df = item_list.value_counts().rename_axis(kind).to_frame(name='counts')
       
        dummy_item = item_freq_df[item_freq_df["counts"]>=threshold]
        dummy_item.reset_index(inplace=True)

        dummy_item = dummy_item[kind]
        dummy_item = dummy_item[dummy_item!=""]
        print(f"print length of the dummy {kind}: {len(dummy_item)}")
        #saving file
        if save_to == "csv":
            dummy_item.to_csv(f'{file_name}.csv',index=False)
            print(f" status:file {file_name}.csv saved")
        elif save_to == "json":
            #reading json file if available
            
            if json_file not in os.listdir():
                with open(json_file,'w') as file:
                    file.write("{}")
            print(json_file,"saved")
            with open(json_file,"r+") as file:
                dummy_data = json.loads(file.read())
                if kind not in dummy_data.keys():
                    dummy_data[kind]={}
                flag = "primary" if threshold == 5 else "secondary"
                dummy_data[kind][flag] = list(dummy_item)
            #save data
            with open(json_file, 'w') as file:  
                  json.dump(dummy_data,file)
            return dummy_data
            
    except Exception as e:
        print("status: error",e)

def generate_dummy_json(files=['email.csv','phone.csv',"social.csv"],path="../",columns=['primary','secondary'],threshold_list=[5,20]):
    
    for file in files:
        file_path = path+file
        for threshold in threshold_list:
            dataframe = pd.read_csv(file_path,index_col=False)
            #transform columns value to map to the dummy_items_collector's columns argument
            col_list = []
            for col in columns:
                col_list.append(col+"_"+file.split(".")[0])
            dummy_items_collector(dataframe,columns=col_list,
                                  threshold=threshold,
                                  save_to="json")
            
            
if __name__ == "__main__":
	generate_dummy_json()
