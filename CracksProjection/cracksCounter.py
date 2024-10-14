import pandas as pd
import json


####### Input Here are dictionaries we wil convert them to dataframe before execution
def startTracking(df,filtered_df):
    
    images_names = list(filtered_df['Potholes'].keys())

    for i in range(len(images_names)):
        cracks_list = filtered_df['Potholes'][images_names[i]]['PotholesData']
        # print(len(cracks_list))
        # if len(cracks_list)<1:
        #     continue
        for j,crack in enumerate(cracks_list):
            backward_count = 0
            forward_count = 0
            ####Forward Count
            if i+1<len(images_names):
                current = i+1
                pothole_num = cracks_list[j]['pothole_num']
                print(pothole_num)
                
                while current<len(images_names):
                    cur_df = pd.DataFrame(df['Potholes'][images_names[current]]['PotholesData'])
                    print(cur_df.head)
                    cur_df = cur_df[cur_df['parent1'] == pothole_num]
                    print(cur_df.head)
                    if len(cur_df)>0:
                        pothole_num = cur_df['pothole_num']
                        print("Check")
                        forward_count+=1
                        current+=1
                    else:
                        break
                    
            
            ####Backward Count
            if (i-1)>=0:
                current = i-1
                pothole_num = cracks_list[j]['pothole_num']
                
                while current>=0:
                    cur_df = pd.DataFrame(df['Potholes'][images_names[current]]['PotholesData'])
                    cur_df = cur_df[cur_df['parent2']==pothole_num]
                    if len(cur_df)>0:
                        print("Check")
                        pothole_num = cur_df['pothole_num']
                        backward_count+=1
                        current-=1
                    else:
                        break

            # print("Done")
            # print(forward_count)
            # print(backward_count)
            filtered_df['Potholes'][images_names[i]]['PotholesData'][j]['forward_count'] = forward_count    
            filtered_df['Potholes'][images_names[i]]['PotholesData'][j]['backward_count'] = backward_count    
                        
    return filtered_df


if __name__ == "__main__":
    print("Starting..................................")

    outputDir = 'Testing'
    
    tracks = json.load(open(f"{outputDir}/tracked_parents.json"))
    filtered_tracks = json.load(open(f"{outputDir}/ProcessedCracks.json"))
    results = startTracking(tracks,filtered_tracks)
    
    for i in results['Potholes']:
        df = pd.DataFrame(results['Potholes'][f"{i}"]['PotholesData'])
        print(df)
        # print(i)
    
    # with open(f"{outputDir}/Final.json", 'w') as file:
    #     json.dump(results, file,indent=4)
    print("Successful................................")
