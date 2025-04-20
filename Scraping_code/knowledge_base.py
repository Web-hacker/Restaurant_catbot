import pandas as pd
import numpy as np
import json
import os

# 🔁 Set the folder containing your 25 CSV files
csv_folder_path = "E:\Dekstop\GenAIProject\Scraping\CSV_data_new"  
knowledge_base = []

def restaurant_data(df):
    df[['Ratings','Delivery_Time','Location']] = 'N/A'
    for idx,item in enumerate(df['rating']):
        lis = item.split('•')
        df['Ratings'][idx] = lis[0]
        df['Delivery_Time'][idx] = lis[1]
    
    for idx,item in enumerate(df['link']):
        df['Location'][idx] = item.replace('https://www.swiggy.com/city/kanpur/','').replace(df['name'][idx].replace(' ','-').lower()+'-','')
    
    df['cleaned_location'] = df['Location'].str.replace(r'rest.*', '', regex=True).str.rstrip('-').str.replace('-',' ')

    return df


def Data_Cleaning(csv_file):
    
    restaurant_location = csv_file["Restaurant_Location"][0]
    csv_file[['Raw_Info','Info','Cusine_Name','Price','Rating','Total_Reviews','Description','Cuisine_type','Tags']] = 'N/A'
    for idx,item in enumerate(csv_file['Complete Info']):
        lis = item.split('\n')
        if len(lis)>=6:
            csv_file['Raw_Info'][idx] = lis
            csv_file['Info'][idx] = lis[0]
            csv_file['Cusine_Name'][idx] = lis[1]
            csv_file['Price'][idx] = lis[2]
            if len(lis[3])<=3 and lis[3]!='ADD':
                csv_file['Rating'][idx] = lis[3]
                csv_file['Total_Reviews'][idx] = lis[4]
            else:
                csv_file['Rating'][idx] = None
                csv_file['Total_Reviews'][idx] = None
            
            #csv_file['Description'][idx] = lis[5]
        elif len(lis)==5:
            csv_file['Raw_Info'][idx] = lis
            csv_file['Info'][idx] = lis[0]
            csv_file['Cusine_Name'][idx] = lis[1]
            csv_file['Price'][idx] = lis[2]
            if len(lis[3])<=3 and lis[3]!='ADD':
                csv_file['Rating'][idx] = lis[3]
                csv_file['Total_Reviews'][idx] = lis[4]
                #csv_file['Description'][idx] = None
            else:
                csv_file['Rating'][idx] = None
                csv_file['Total_Reviews'][idx] = None
                #csv_file['Description'][idx] = lis[3]
        else:
            csv_file['Raw_Info'][idx] = lis
            csv_file['Info'][idx] = lis[0]
            csv_file['Cusine_Name'][idx] = lis[1]
            csv_file['Price'][idx] = lis[2]
            csv_file['Rating'][idx] = None
            csv_file['Total_Reviews'][idx] = None
            #csv_file['Description'][idx] = lis[3]

    csv_file['AfterDescription'] = csv_file['Info'].str.extract(r'(?i)Description:\s+(.*?)\s+Swipe', expand=False)

    csv_file.loc[csv_file['AfterDescription'].isnull() == True,'AfterDescription'] = None

    csv_file.loc[csv_file['Description'] == 'ADD', 'Description'] = None
    csv_file.loc[csv_file['Description'] == 'more', 'Description'] = None
    csv_file.loc[csv_file['Description'] == 'Customisable', 'Description'] = None
    
    for idx,item in enumerate(csv_file['Info']):
        lis = item.split('.')
        csv_file['Cuisine_type']=lis[0]
    
    
    for idx,item in enumerate(csv_file['Complete Info']):
        lis=[]
        if "Bestseller" in item:
            lis.append("Bestseller")
        if "Must Try" in item:
            lis.append("Must Try")
        if len(lis)!=0:
            csv_file['Tags'][idx]=lis
        else:
            csv_file['Tags'][idx]=None

    return csv_file,restaurant_location


restaurant_csv_file = pd.read_csv("swiggy_restaurants_kanpur.csv")
restaurant_info_file = restaurant_data(restaurant_csv_file)

# 🔄 Iterate through all CSVs in the folder
for file in os.listdir(csv_folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(csv_folder_path, file)
        
        # Extract restaurant name from filename
        restaurant_name = file.replace("_dishes.csv", "").replace(".csv", "").replace("_", " ").strip().title()
        print(f"Preparing Knowledge Base for {restaurant_name}")

        restaurant_info = restaurant_info_file[restaurant_info_file['name'].str.lower() == restaurant_name.lower()]

        restaurant_menus=[]

        restaurant_location=None

        try:
            file = pd.read_csv(file_path)
            
            df, restaurant_location = Data_Cleaning(file)

            # 🧼 Normalize column names (in case they're inconsistent)
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

            # 🧱 Build structured entries
            for _, row in df.iterrows():
                menu = {
                    "dish_name": row.get("cuisine_name", ""),
                    "description": row.get("afterdescription", "") ,
                    "price": row.get("price", ""),
                    "rating": row.get("rating", ""),
                    "num_reviews": row.get("total_reviews", ""),
                    "dish_type": row.get("cuisine_type", ""),
                    "tags": row.get("tags", ""),
                    "dish_tags": row.get("dish_tags","")
                }
                restaurant_menus.append(menu)

        except Exception as e:
            print(f"Error processing {file}: {e}")
        
        for _, row in restaurant_info.iterrows():
            entry = {
                    "restaurant_name": row.get("name", ""),
                    "available_cuisine": row.get("cuisine", "") ,
                    "delivery_time": row.get("Delivery_Time", ""),
                    "restaurant_rating": row.get("Ratings", ""),
                    "city": row.get("city", ""),
                    "restaurant_location": restaurant_location,
                    "restaurant_menu":restaurant_menus
                }
            knowledge_base.append(entry)
        print(f"Total entry in restaurant menus after reading {restaurant_name} is {len(restaurant_menus)}")
        print(f"Total entry in knowledge base after reading {restaurant_name} is {len(knowledge_base)}")

# 💾 Save combined knowledge base to JSON
output_path = os.path.join(csv_folder_path, "new_combined_knowledge_base.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(knowledge_base, f, indent=4, ensure_ascii=False)

print(f"✅ Combined knowledge base saved at: {output_path}")
